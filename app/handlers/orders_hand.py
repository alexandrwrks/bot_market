from aiogram import F, Router, types

from app.keyboards.orders import get_user_orders

router = Router()


@router.callback_query(F.data == "orders_btn")
async def get_orders(callback: types.CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text="Ваши заказы:",
        reply_markup=get_user_orders(),
    )
