from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup

from app.keyboards.basket import get_user_basket
from app.repo.basket import basket_repo
from app.repo.orders import order_repo
from app.repo.products import product_repo

router = Router()


async def _render_basket(callback: CallbackQuery) -> None:
    telegram_id = callback.from_user.id
    total_price = await basket_repo.get_active_basket_total_price(telegram_id)
    items = await basket_repo.get_active_user_basket(telegram_id)

    if not items:
        text = (
            "Ваша корзина пуста.\n"
            "Минимальная сумма заказа - 5000 RUB."
        )
    else:
        lines = ["Ваша корзина:"]
        for name, quantity, price in items:
            lines.append(f"- {name}: {quantity} x {price} RUB")

        lines.append("")
        lines.append(f"Сумма товаров: {total_price} RUB")
        lines.append("Минимальная сумма заказа - 5000 RUB.")
        text = "\n".join(lines)
        
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=get_user_basket(),
        )
    except Exception:
        await callback.message.answer(
            text=text,
            reply_markup=get_user_basket()
        )


@router.callback_query(F.data == "basket_btn")
async def get_basket(callback: CallbackQuery):
    await callback.answer()
    await _render_basket(callback)


@router.callback_query(F.data == "basket_composition_btn")
async def basket_composition(callback: CallbackQuery):
    await callback.answer()
    await _render_basket(callback)


@router.callback_query(F.data == "clear_btn")
async def clear_basket(callback: CallbackQuery):
    deleted = await basket_repo.clear_basket(callback.from_user.id)
    if deleted:
        await callback.answer("Корзина очищена")
    else:
        await callback.answer("Корзина уже пуста")

    await _render_basket(callback)


@router.callback_query(F.data == "confirm_order_btn")
async def confirm_order(callback: CallbackQuery):
    order = await order_repo.create_order_from_active_basket(callback.from_user.id)
    if order is None:
        await callback.answer("Не удалось оформить заказ. Корзина пуста или товара недостаточно.", show_alert=True)
        return

    await callback.answer(f"Заказ №{order.id} оформлен")
    await _render_basket(callback)


"""
Пользоватлеь нажимает на кнопку "Добавить в корзину"
Сделать так чтобы пользователь писал своё число товаров которое ему нужно
"""
@router.callback_query(F.data.startswith("add_to_cart:"))
async def add_product_to_basket(callback: CallbackQuery):
    await callback.answer()

    product_id = callback.data.split(":")[1]
    telegram_id = callback.from_user.id
    
    product = await product_repo.get_product_by_id(product_id)

    await callback.message.answer(
        text=(
            f"{product.name} успешно добавлена в корзину"
        )
    )

    await basket_repo.add_product_to_basket(
        telegram_id=telegram_id,
        product_id=product_id,
        price=product.price,
        quantity=1
    )
    
    await product_repo.update_product_quantity(
        product_id=product_id,
        quantity=1
    )

