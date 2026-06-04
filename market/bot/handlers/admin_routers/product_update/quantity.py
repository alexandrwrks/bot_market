from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from market.bot.exception.product_ex import NotFoundProductError
from market.bot.keyboards.admin_keyboards.product_update import (
    get_options_for_changes,
    get_access_options_quantity,
)
from market.bot.keyboards.admin_keyboars import get_admin_inline_keyboard
from market.bot.service.admin_service import admin_service
from market.bot.service.product_service import product_service

router = Router()


from aiogram.fsm.state import State, StatesGroup

class QuantityChange(StatesGroup):
    new_quantity = State()

@router.callback_query(F.data.startswith("quantity_change:"))
async def process_price_change(callback: CallbackQuery, state: FSMContext):
    try:
        parts = callback.data.split(":")

        slug = parts[1]
        product_id = int(parts[2])

        await state.update_data(
            slug=slug,
            product_id=product_id,
        )
        await state.set_state(QuantityChange.new_quantity)

        await callback.answer()
        await callback.message.answer(text="Напишите новое количество:")

    except Exception as e:
        await callback.answer(
            text="Ошибка изменения количества. Попробуйте позже.",
            show_alert=True,
        )

@router.message(QuantityChange.new_quantity)
async def process_new_price(message: Message, state: FSMContext):
    try:
        new_quantity = int(message.text)

        if new_quantity < 0:
            raise ValueError

    except ValueError:
        await message.answer("Введите корректное количество числом")
        return

    await state.update_data(new_quantity=new_quantity)

    await message.answer(
        text=f"Количество товара: {new_quantity}",
        reply_markup=get_access_options_quantity()
    )

@router.callback_query(F.data == "access_quantity_change")
async def access_price_change(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()

        await admin_service.set_access_quantity(
            product_id=data["product_id"],
            new_quantity=data["new_quantity"],
        )

        await state.clear()

        await callback.message.answer("Успешное изменения количества!")

        product = await product_service.get_product_information(product_id=data["product_id"])

        caption = (
            f"{product.name}\n\n"
            f"Описание: {product.description}\n\n"
            f"Цена: {product.price} руб.\n"
            f"В наличии: {product.quantity} шт."
        )

        await callback.answer()
        await callback.message.answer_photo(
            photo=FSInputFile(product.photo_path),
            caption=caption,
            reply_markup=get_options_for_changes(slug=data["slug"], product_id=data["product_id"]),
        )

    except NotFoundProductError:
        await callback.message.answer(
            text="Панель администратора",
            reply_markup=get_admin_inline_keyboard(),
        )

    except Exception:
        await callback.answer(
            text="Ошибка обновления количества",
            show_alert=True,
        )

@router.callback_query(F.data == "delete_quantity_change")
async def delete_price_change(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await state.clear()

        await callback.message.answer(text="Отмена изменения количества")

        product = await product_service.get_product_information(product_id=data["product_id"])

        caption = (
            f"{product.name}\n\n"
            f"Описание: {product.description}\n\n"
            f"Цена: {product.price} руб.\n"
            f"В наличии: {product.quantity} шт."
        )

        await callback.answer()
        await callback.message.answer_photo(
            photo=FSInputFile(product.photo_path),
            caption=caption,
            reply_markup=get_options_for_changes(slug=data["slug"], product_id=data["product_id"]),
        )

    except (Exception, NotFoundProductError):
        await callback.message.answer(
            text="Панель администратора",
            reply_markup=get_admin_inline_keyboard(),
        )