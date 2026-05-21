from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_inline_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Каталог", callback_data="catalog_btn")
    keyboard.button(text="Корзина", callback_data="basket_btn")
    keyboard.button(text="Заказы", callback_data="orders_btn")

    return keyboard.as_markup()


def get_admin_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Добавить товары", callback_data="admin_products")
    keyboard.button(text="Посмотреть заказы", callback_data="admin_orders")
    keyboard.button(text="Посмотреть статистику", callback_data="admin_statistics")

    return keyboard.adjust(1).as_markup()
