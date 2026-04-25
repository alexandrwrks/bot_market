from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.basket import get_user_basket
from app.repo.basket import basket_repo
from app.repo.orders import order_repo

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

    await callback.message.edit_text(
        text=text,
        reply_markup=get_user_basket(),
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
