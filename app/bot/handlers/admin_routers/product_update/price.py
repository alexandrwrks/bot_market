from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.bot.exception.product_ex import NotFoundProductError
from app.bot.fsm.fsms import PriceChange
from app.bot.keyboards.admin_keyboards.product_update import (
    get_access_options, get_admin_products_keyboard,
    get_exists_catalog_for_admin, get_options_for_changes)
from app.bot.service.admin_service import admin_service
from app.bot.service.category_service import category_service
from app.bot.service.product_service import product_service
from app.utils import logger

router = Router()

"""
Usage MVP

router: admin_update_products
get all categories, every category have slug

router: admin_category:{slug}
get all products by slug

router: admin_product:{slug}:{product_id}
get product info bu product_id
"""


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

        keyboard = get_exists_catalog_for_admin(categories)

        await callback.answer()
        try:
            await callback.message.edit_text(
                text="📱 Выберите категорию:",
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

@router.callback_query(F.data.startswith("admin_panel:change:price"))
async def process_price_change(callback: CallbackQuery, state: FSMContext):
    try:
        parts = callback.data.split(":")

        slug = parts[-2]
        product_id = int(parts[-1])

        await state.update_data(
            slug=slug,
            product_id=product_id,
        )

        await state.set_state(PriceChange.new_price)

        await callback.answer()
        await callback.message.answer(text="Напишите новую цену:")

    except Exception as e:
        logger.error("Ошибка изменения цены товара %s", e)

        await callback.answer(
            text="❌ Ошибка изменения цены. Попробуйте позже.",
            show_alert=True,
        )
        return

@router.message(PriceChange.new_price)
async def process_new_price(message: Message, state: FSMContext):
    try:
        new_price = int(message.text)

        if new_price < 0:
            raise ValueError

        await state.update_data(new_price=new_price)

        await message.answer(
            text=f"💰 Новая цена товара: {new_price}", reply_markup=get_access_options()
        )

    except ValueError:
        await message.answer("Введите корректную цену числом")
        return


@router.callback_query(F.data == "change:access_price")
async def access_price_change(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()

        await admin_service.set_access_price(
            product_id=data["product_id"],
            new_price=data["new_price"],
        )

        await state.clear()

        await callback.answer()

        await callback.message.answer("✅ Успешное обновление цены")

        product = await product_service.get_product_information(
            product_id=data["product_id"]
        )

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
            reply_markup=get_options_for_changes(
                slug=data["product_id"], product_id=data["product_id"]
            ),
        )

    except Exception as e:
        logger.error("Ошибка обновления цены %s", e)

        await callback.answer(
            text="❌ Ошибка обновления цены",
            show_alert=True,
        )
        return

@router.callback_query(F.data == "change:delete_price")
async def delete_price_change(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await state.clear()

    await callback.answer()
    await callback.message.answer(
        text="✖️ Отмена изменения цены",
        reply_markup=get_options_for_changes(
            slug=data["slug"],
            product_id=data["product_id"],
        ),
    )
