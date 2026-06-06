from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_inline_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📂 Каталог", callback_data="menu:catalog")
    keyboard.button(text="🗑 Корзина", callback_data="menu:basket")
    keyboard.button(text="🗳 Заказы", callback_data="menu:orders")

    return keyboard.as_markup()
