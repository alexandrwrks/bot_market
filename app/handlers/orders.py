from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboards.orders import get_user_orders
from app.repo.orders import order_repo

router = Router()


@router.callback_query(F.data == "orders_btn")
async def get_orders(callback: CallbackQuery):
    await callback.answer()

    orders = await order_repo.get_user_orders(callback.from_user.id)
    order_rows = [(order.id, order.total_price, order.status) for order in orders]

    if not order_rows:
        text = "У вас пока нет заказов."
    else:
        text = "Ваши заказы:"

    await callback.message.edit_text(
        text=text,
        reply_markup=get_user_orders(order_rows),
    )


@router.callback_query(F.data.startswith("order:"))
async def get_order_details(callback: CallbackQuery):
    await callback.answer()

    try:
        order_id = int(callback.data.split(":", maxsplit=1)[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный номер заказа", show_alert=True)
        return

    order = await order_repo.get_order_by_id(callback.from_user.id, order_id)
    if order is None:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    await callback.message.edit_text(
        text=(
            f"Заказ №{order.id}\n"
            f"Статус: {order.status}\n"
            f"Сумма: {order.total_price} RUB"
        ),
        reply_markup=get_user_orders([(order.id, order.total_price, order.status)]),
    )
