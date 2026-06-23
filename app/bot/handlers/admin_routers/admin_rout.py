from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.bot.exception.admin_ex import OrdersNotEnough
from app.bot.exception.product_ex import NotFoundProductError
from app.bot.exception.user_ex import NotFoundUserError, UserAdminLicense
from app.bot.keyboards.admin_keyboards.product_update import (
    get_admin_products_keyboard,
    get_exists_catalog_for_admin,
    get_options_for_changes,
)
from app.bot.keyboards.admin_keyboars import (
    access_product_delete,
    get_admin_inline_keyboard,
    get_back_admin_keyboard,
)
from app.bot.keyboards.start import get_start_inline_keyboard
from app.bot.service.admin_service import admin_service
from app.bot.service.category_service import category_service
from app.bot.service.product_service import product_service
from app.bot.service.user_service import user_service
from app.utils import logger

router = Router()

WELCOME_MESSAGE = "Панель администратора\nВыберите действие:"


@router.message(Command("admin"))
async def admin_command(message: Message):
    try:
        await user_service.admin_panel(message.from_user.id)

        await message.answer(
            text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
        )

    except UserAdminLicense:
        await message.answer(
            text="У Вас отсутствуют права администратора",
            reply_markup=get_start_inline_keyboard(),
        )
        return

    except NotFoundUserError:
        await message.answer(
            text="Команда не временно не работает. Попробуйте позже",
            reply_markup=get_start_inline_keyboard(),
        )
        return

    except Exception:
        await message.answer(
            text="❌ Ошибка со стороны сервера. Попробуйте позже.",
            reply_markup=get_start_inline_keyboard(),
        )
        return


@router.callback_query(F.data == "admin_panel:menu")
async def admin_panel_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
    )


@router.callback_query(F.data == "admin_admin:orders:view")
async def admin_orders_callback(callback: CallbackQuery):
    await callback.answer()
    """
    Просмотр всех новых заказов которые появились,
    кроме → отменённых и доставленных/выполненных
    """
    try:
        orders = await admin_service.get_admin_orders()

        await callback.message.delete()
        for order in orders:
            text = (
                f"НОМЕР ЗАКАЗА №{order.number}\n"
                f"Имя пользователя: {order.full_name}\n"
                f"Номер телефона: {order.phone}\n"
                f"Стоимость заказа: {order.total_price}\n"
                f"Статус заказа: {order.status.value}"
            )

            await callback.message.answer(text=text)

        await callback.message.answer(
            text="Выберите следующие действие:",
            reply_markup=get_back_admin_keyboard(),
        )

    except OrdersNotEnough:
        await callback.message.answer(
            text="Новые заказы отсутствуют", reply_markup=get_back_admin_keyboard()
        )

    except Exception:
        await callback.message.answer(
            text="❌ Ошибка сервера. Попробуйте позже.",
            reply_markup=get_back_admin_keyboard(),
        )


@router.callback_query(F.data == "admin_admin:statistics:view")
async def admin_statistics_callback(callback: CallbackQuery):
    await callback.answer()
    """
    Показ статистики бота:
    1) количество заказов
    2) количество новых пользователей
    """
    try:
        admin_info = await admin_service.get_admin_info()
        keyboard = get_back_admin_keyboard()

        text = (
            f"\tСтатистика:\n"
            f"Пользователи: {admin_info.users}\n"
            f"Заказы: {admin_info.orders}"
        )

        try:
            await callback.message.edit_text(text=text, reply_markup=keyboard)

        except TelegramBadRequest:
            await callback.message.delete()

            await callback.message.answer(text=text, reply_markup=keyboard)

    except Exception:
        await callback.answer(
            text="❌ Ошибка сервера",
            show_alert=True,
        )


@router.callback_query(F.data.startswith("admin_panel:change:delete:"))
async def change_delete_callback(callback: CallbackQuery):
    try:
        parts = callback.data.split(":")

        slug = parts[-2]
        product_id = int(parts[-1])

        await callback.message.answer(
            text="Подтвердите действие",
            reply_markup=access_product_delete(slug, product_id),
        )

    except Exception:
        await callback.answer(
            text="❌ Ошибка удаления товара",
            show_alert=True,
        )
        return


@router.callback_query(F.data.startswith("admin_panel:product:delete"))
async def delete_product_callback(callback: CallbackQuery):
    try:
        parts = callback.data.split(":")

        slug = parts[-3]
        product_id = int(parts[-2])

        action = parts[-1]

        """
        TODO: сделать условие на то какое значение будет в конце то действие и будет происходить
        Если 1 то удаляем если 0 то оставляем
        """
        await callback.message.delete()
        if action == "cancel":
            await callback.message.answer("✖️ Удаление товара отменено")

            await callback.message.answer(
                text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
            )

        elif action == "confirm":
            product_name = await admin_service.delete_product(product_id=product_id)

            if product_name is not None:
                await callback.message.answer(
                    f"✅ Успешное удаление товара: {product_name}"
                )
            else:
                await callback.message.asnwer("✅ Успешное удаление товара")

            await callback.message.answer(
                text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
            )

    except Exception:
        await callback.message.delete()
        await callback.answer(
            text="❌ Ошибка удаления товара",
            show_alert=True,
        )
        return


@router.callback_query(F.data == "admin_panel:products:update")
async def admin_update_products_callback(callback: CallbackQuery):
    """
    Выбор продукта как у пользователя,
    только после чего идут кнопки на выбор обновления данных:
    Выдать категории → выдать товар по этой категории →
    → нажать на кнопку изменения чего-то

    Выбор изменений: цена, количество, фото, описание, удаление товара(мягкое),
    """
    try:
        categories = await category_service.get_categories()

        text = "📱 Выберите категорию:"
        keyboard = get_exists_catalog_for_admin(categories)

        await callback.answer()
        try:
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
            )

        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=keyboard,
            )

    except Exception as e:
        logger.error("Ошибка выдачи категорий %s", e)
        await callback.answer(
            text="❌ Ошибка выдачи категорий. Попробуйте позже.",
            show_alert=True,
        )
        return


@router.callback_query(F.data.startswith("admin_panel:catalog:category:"))
async def process_admin_category(callback: CallbackQuery):
    slug = callback.data.split(":")[-1]
    try:
        products = await product_service.get_products_by_category(slug=slug)

        text = "📱 Выберите товар:"
        keyboard = get_admin_products_keyboard(products, slug)

        await callback.answer()
        try:
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
            )

        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=keyboard,
            )

    except Exception as e:
        logger.error("Ошибка получения товара по категории %s", e)

        await callback.answer(
            text=f"❌ Ошибка выдачи товара по категории {slug}",
            show_alert=True,
        )
        return


@router.callback_query(F.data.startswith("admin_panel:catalog:products:"))
async def process_admin_product(callback: CallbackQuery):
    try:
        parts = callback.data.split(":")

        slug = parts[3]
        product_id = int(parts[4])

        product = await product_service.get_product_information(product_id=product_id)

        caption = (
            f"{product.name}\n\n"
            f"{product.description}\n\n"
            f"💰 Стоимость: {product.price} RUB за 1 шт.\n"
            f"В наличии: {product.quantity} шт."
        )

        await callback.answer()
        await callback.message.answer_photo(
            photo=FSInputFile(product.photo_path),
            caption=caption,
            reply_markup=get_options_for_changes(slug=slug, product_id=product_id),
        )

    except (Exception, NotFoundProductError) as e:
        logger.error("Ошибка получения товара %s", e)

        await callback.answer(
            text="❌ Ошибка получения товара. Попробуйте позже.",
            show_alert=True,
        )
        return
