from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.orders import get_pay_order
from app.bot.service.order_service import order_service
from app.utils import logger

router = Router()


@router.callback_query(F.data.startswith("order:done"))
async def confirm_order(callback: CallbackQuery):
    try:
        order_id, total_price = await order_service.create_order(callback.from_user.id)
        text = (
            f"✅ Заказ создан!\n"
            f"Номер заказа: {order_id}\n"
            f"Сумма: {total_price} RUB\n\n"
            f"Нажмите «💳 Оплатить», затем «🔄 Проверить оплату»."
        )

        # payment_url = order.payment_url
        payment_url = "https://www.google.com"

        await callback.answer()
        await callback.message.answer(
            text=text,
            reply_markup=get_pay_order(payment_url),
        )

    except Exception as e:
        logger.exception(e)
        await callback.answer(
            text="❌ Ошибка создания заказа",
            show_alert=True,
        )
