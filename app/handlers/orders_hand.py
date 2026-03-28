from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards.orders import get_user_orders

router = Router()

@router.callback_query(F.data == "orders_btn")
async def get_orders(
    callback: CallbackQuery
):
    text1 = ("У вас пока что нет активных заказов!")
    text2 = ("Ваши заказы: ")
    """Проверка наличия заказов у пользователя"""
    
    await callback.message.answer(
        text=text2,
        reply_markup=get_user_orders()
    )

    await callback.answer()