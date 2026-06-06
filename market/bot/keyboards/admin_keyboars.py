from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_back_admin_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Вернуться в главное меню", callback_data="admin_panel:menu")

    return keyboard.adjust(1).as_markup()


def get_admin_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➕ Добавить товары", callback_data="admin_panel:products:add")
    keyboard.button(text="🔄 Обновить товары", callback_data="admin_panel:products:update")
    keyboard.button(text="📈 Посмотреть заказы", callback_data="admin_admin:orders:view")
    keyboard.button(text="📊 Посмотреть статистику", callback_data="admin_admin:statistics:view")

    return keyboard.adjust(1).as_markup()


def get_different_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Вернуться в главное меню", callback_data="admin_panel:menu")

    return keyboard.adjust(1).as_markup()
