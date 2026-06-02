from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_user_orders(orders):
    keyboard = InlineKeyboardBuilder()

    if orders:
        for order_id, total_price, status in orders:
            keyboard.button(
                text=f"Заказ №{order_id} ({total_price} RUB, {status})",
                callback_data=f"order:{order_id}",
            )

    keyboard.button(text="🔙 Назад", callback_data="back_one_start")
    return keyboard.adjust(1).as_markup()


def get_basket_and_catalog():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🗑 Корзина", callback_data="basket_btn")
    keyboard.button(text="📂 Каталог", callback_data="catalog_btn")

    return keyboard.adjust(2).as_markup()


def get_confirm_order():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="❌ Сделать изменения", callback_data="changes_btn")
    keyboard.button(text="✅ Подтвердить", callback_data="done_btn")

    return keyboard.adjust(2).as_markup()


def get_detail_keyboard(order_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Подробнее", callback_data=f"detail_order:{order_id}")

    return keyboard.adjust(1).as_markup()