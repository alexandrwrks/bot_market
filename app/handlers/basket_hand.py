from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards.basket import get_user_basket

router = Router()

@router.callback_query(F.data == "basket_btn")
async def get_basket(
    callback: CallbackQuery
):
    """Подсчитать сумму товаров для каждого польщователя"""
    await callback.answer()

    text = ("Ваша корзина\n"
            "Сумма товаров:\n"
            "Доставка СДЭК:\n"
            "Минимальная сумма заказа - 5000 рублей\n")

    await callback.message.edit_text(
        text=text,
        reply_markup=get_user_basket()
    )
