from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.orders import get_pay_order
from app.bot.service.order_service import order_service

router = Router()


@router.callback_query(F.data.startswith("order:confirm"))
async def confirm_order(callback: CallbackQuery):
    try:
        order = await order_service.get_order()
        text = (
            f"✅ Заказ создан!\n"
            f"Номер заказа: {order.id}\n"
            f"Сумма: {order.total_price} RUB\n\n"
            f"Нажмите «💳 Оплатить», затем «🔄 Проверить оплату»."
        )

        payment_url = order.payment_url

        await callback.answer()
        await callback.message.answer(
            text=text,
            reply_markup=get_pay_order(payment_url),
        )

    except Exception:
        await callback.answer(
            text="❌ Ошибка создания заказа",
            show_alert=True,
        )
