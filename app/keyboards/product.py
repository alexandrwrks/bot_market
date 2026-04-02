from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_product_keyboard():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➕ Добавить в корзину", callback_data="add_to_cart")
    keyboard.button(text="🔄 Выбрать другой вкус", callback_data="back_one")
    keyboard.button(text="🔙 Вернуться в категории", callback_data="back_to_categories")
    keyboard.button(text="🛒 Корзина", callback_data="basket_composition_btn")

    return keyboard.adjust(1).as_markup()