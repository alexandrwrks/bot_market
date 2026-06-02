from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from fastapi import Depends

from market.bot.exception.admin_ex import AdminInfoError
from market.bot.exception.product_ex import NotFoundProductError
from market.bot.exception.user_ex import UserAdminLicense, NotFoundUserError
from market.bot.keyboards.admin_keyboars import (
    get_back_admin_keyboard,
    get_admin_inline_keyboard, get_different_keyboard,
)
from market.bot.keyboards.categories import get_exists_catalog_for_admin
from market.bot.keyboards.product import get_admin_products_keyboard, get_options_for_changes
from market.bot.keyboards.start import get_start_inline_keyboard
from market.bot.service.admin_service import admin_service, AdminInfo
from market.bot.service.category_service import category_service
from market.bot.service.product_service import product_service
from market.bot.service.user_service import user_service

router = Router()

WELCOME_MESSAGE = "Панель администратора\nВЫберите действие:"


@router.message(Command("admin"))
async def admin_command(message: Message):
    try:
        await user_service.admin_panel(message.from_user.id)

        await message.answer(
            text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
        )

    except UserAdminLicense:
        await message.answer(
            text="У Вас нет прав на использование админки",
            reply_markup=get_start_inline_keyboard(),
        )

    except NotFoundUserError:
        await message.answer(
            text="Команда не временно не работает. Попробуйте позже",
            reply_markup=get_start_inline_keyboard(),
        )

    except Exception:
        await message.answer(
            text="Ошибка со стороны сервера. Попробуйте позже.",
            reply_markup=get_start_inline_keyboard(),
        )


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
    )


@router.callback_query(F.data == "admin_products")
async def admin_products_callback(callback: CallbackQuery):
    """
    Добавить FSM для добавления товара:
    1) выбор категории → добавляем новую если её нет в БД
    2) FSM для написания данных о товаре
    3) подтверждение добавления товара
    """
    await callback.answer()
    await callback.message.edit_text(
        text="Добавление товаров находится в разработке. Попробуйте позже.",
        reply_markup=get_back_admin_keyboard(),
    )


@router.callback_query(F.data == "admin_update_products")
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

        await callback.answer()
        await callback.message.edit_text(
            text="Выберите категорию:",
            reply_markup=get_exists_catalog_for_admin(categories),
        )

    except Exception:
        await callback.answer(
            text="Ошибка выдачи категорий. Попробуйте позже.",
            show_alert=True,
        )

@router.callback_query(F.data.startswith("admin_category:"))
async def process_admin_category(callback: CallbackQuery):
    slug = callback.data.split(":")[1]
    try:
        products = await product_service.get_products_by_category(slug=slug)

        try:
            await callback.message.edit_text(
                text="Выберите товар:",
                reply_markup=get_admin_products_keyboard(products, slug)
            )

        except TelegramBadRequest:
            await callback.message.answer(
                text="Выберите товар:",
                reply_markup=get_admin_products_keyboard(products, slug)
            )

    except Exception:
        print("Ошибка на уровне Exception")
        await callback.answer(
            text=f"Ошибка выдачи товаров по категории",
            show_alert=True,
        )

@router.callback_query(F.data.startswith("admin_product"))
async def process_admin_product(callback: CallbackQuery):
    parts = callback.data.split(":")

    slug = parts[1]
    product_id = int(parts[2])

    try:
        product = await product_service.get_product_information(product_id=product_id)

        caption = (
            f"{product.name}\n\n"
            f"Описание: {product.description}\n\n"
            f"Цена: {product.price} руб.\n"
            f"В наличии: {product.quantity} шт."
        )

        await callback.message.answer_photo(
            photo=FSInputFile(product.photo_path),
            caption=caption,
            reply_markup=get_options_for_changes(slug=slug, product_id=product_id)
        )

    except NotFoundProductError:
        await callback.answer(
            text="Ошибка выдачи товара. Попробуйте позже.",
            show_alert=True,
        )

    except Exception:
        await callback.answer(
            text="Ошибка получения товара. Попробуйте позже.",
            show_alert=True,
        )


@router.callback_query(F.data == "admin_orders")
async def admin_orders_callback(callback: CallbackQuery):
    await callback.answer()
    """
    Просмотр всех новых заказов которые появились,
    кроме → отменённых и доставленных/выполненных
    """
    try:
        orders = await admin_service.get_admin_orders()

        for order in orders:
            text = (
                f"НОМЕР ЗАКАЗА №{order.number}\n"
                f"Имя пользователя: {order.name}\n"
                f"Номер телефона: {order.phone}\n"
                f"Стоимость заказа: {order.total_price}\n"
                f"Статус заказа: {order.status.value}"
            )

            await callback.message.answer(text=text)

        await callback.message.answer(
            text="Выберите следующие действие:",
            reply_markup=get_back_admin_keyboard(),
        )


    except Exception:
        await callback.message.answer(
            text="Ошибка сервера. Попробуйте позже.",
            reply_markup=get_back_admin_keyboard(),
        )


@router.callback_query(F.data == "admin_statistics")
async def admin_statistics_callback(callback: CallbackQuery):
    await callback.answer()
    """
    Показ статистики бота:
    1) количество заказов
    2) количество новых пользователей
    """
    try:
        admin_info = await admin_service.get_admin_info()

        text = (
            f"\tСтатистика:\n"
            f"Пользователи: {admin_info.users}\n"
            f"Заказы: {admin_info.orders}"
        )

        try:
            await callback.message.edit_text(
                text=text,
                reply_markup=get_different_keyboard(),
            )

        except TelegramBadRequest:
            await callback.message.answer(
                text=text,
                reply_markup=get_different_keyboard(),
            )

    except Exception:
        await callback.answer(
            text="Ошибка сервера",
            show_alert=True,
        )
