from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_user_orders(orders: list[tuple[int, int, str]]):
    keyboard = InlineKeyboardBuilder()

    if orders:
        for order_id, total_price, status in orders:
            keyboard.button(
                text=f"Заказ №{order_id} ({total_price} RUB, {status})",
                callback_data=f"order:{order_id}",
            )

    keyboard.button(text="Назад", callback_data="back_one_start")
    return keyboard.adjust(1).as_markup()
