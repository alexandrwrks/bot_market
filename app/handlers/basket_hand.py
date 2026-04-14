from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.db_repo.basket import basket_repo
from app.keyboards.basket import get_user_basket

router = Router()


@router.callback_query(F.data == "basket_btn")
async def get_basket(callback: CallbackQuery):
    await callback.answer()

    items, total = await basket_repo.get_basket_summary(callback.from_user.id)

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
        lines.append(f"Сумма товаров: {total} RUB")
        lines.append("Минимальная сумма заказа - 5000 RUB.")
        text = "\n".join(lines)

    await callback.message.edit_text(
        text=text,
        reply_markup=get_user_basket(),
    )


@router.callback_query(F.data == "basket_composition_btn")
async def basket_composition(callback: CallbackQuery):
    await get_basket(callback)


@router.callback_query(F.data == "clear_btn")
async def clear_basket(callback: CallbackQuery):
    await callback.answer("Очистка корзины будет добавлена на следующем этапе")


@router.callback_query(F.data == "confirm_order_btn")
async def confirm_order(callback: CallbackQuery):
    await callback.answer("Оформление заказа пока в разработке")
