from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.admin_routers.order_command import OrderCreateSchema


def get_user_orders(orders):
    keyboard = InlineKeyboardBuilder()

    if orders:
        for order_id, total_price, status in orders:
            keyboard.button(
                text=f"Заказ №{order_id} ({total_price} RUB, {status})",
                callback_data=f"order:view:{order_id}",
            )

    keyboard.button(text="🗑 Корзина", callback_data="menu:basket")
    return keyboard.adjust(1).as_markup()


def get_basket_and_catalog():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🗑 Корзина", callback_data="menu:basket")
    keyboard.button(text="📂 Каталог", callback_data="menu:catalog")

    return keyboard.adjust(2).as_markup()


def get_confirm_order():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="❌ Сделать изменения", callback_data="order:changes")
    keyboard.button(text="✅ Подтвердить", callback_data="order:done")

    return keyboard.adjust(2).as_markup()


def get_detail_keyboard(order_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Подробнее", callback_data=f"order:detail:{order_id}")

    return keyboard.adjust(1).as_markup()


def get_pay_order(payment_url: str):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="💳 Оплатить", url=payment_url)
    keyboard.button(text="🔄 Проверить оплату", callback_data="payment:verify")
    keyboard.button(text="🗑 Корзина", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()


def get_back_to_confirm_order():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🔙 Назад", callback_data="order:confirm")

    return keyboard.adjust(1).as_markup()


def get_order_information(user_info: OrderCreateSchema):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=("🔄 Изменить адрес" if user_info.address else "➕ Добавить адрес"),
        callback_data=f"order:change_address"
    )
    keyboard.button(
        text=("🔄 Изменить ФИО" if user_info.full_name else "➕ Добавить ФИО"),
        callback_data=f"order:change_full_name"
    )
    keyboard.button(
        text=("🔄 Изменить телефон" if user_info.phone else "➕ Добавить телефон"),
        callback_data=f"order:change_phone"
    )
    keyboard.button(text="🔙 Назад", callback_data="menu:basket")
    keyboard.button(text="✅ Подтвердить", callback_data=f"order:done")

    return keyboard.adjust(1).as_markup()