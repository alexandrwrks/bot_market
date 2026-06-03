from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_back_admin_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Вернуться в главное меню", callback_data="back_to_admin")

    return keyboard.adjust(1).as_markup()


def get_admin_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➕ Добавить товары", callback_data="admin_products")
    keyboard.button(text="🔄 Обновить товары", callback_data="admin_update_products")
    keyboard.button(text="📈 Посмотреть заказы", callback_data="admin_orders")
    keyboard.button(text="📊 Посмотреть статистику", callback_data="admin_statistics")

    return keyboard.adjust(1).as_markup()


def get_different_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Изменить товары", callback_data="choice_products")
    keyboard.button(text="Вернуться в главное меню", callback_data="back_to_admin")

    return keyboard.adjust(1).as_markup()
