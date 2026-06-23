from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.schemas.fsm.fsms import PriceChange
from app.bot.keyboards.admin_keyboards.product_update import (
    get_access_options,
    get_options_for_changes,
)
from app.bot.service.admin_service import admin_service
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
