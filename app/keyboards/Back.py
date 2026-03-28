from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

def back_to_protein():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="🔙назад", callback_data="back_protein")
    keyboard.button(text="🛒В корзину", callback_data="add_to_cart")

    return keyboard.adjust(2).as_markup()