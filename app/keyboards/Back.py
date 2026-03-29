from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder


def back_to_one():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="🔄Поменять вкус", callback_data="back_one")

    return keyboard.adjust().as_markup()

def put_it_inside():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="🛒В корзину", callback_data="add_to_cart")

    return keyboard.adjust().as_markup()

def back_to_one_start():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="🔙назад", callback_data="back_one_start")

    return keyboard.adjust().as_markup()

def back_to_one_company():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="🔙назад", callback_data="back_one_company")

    return keyboard.adjust().as_markup()

def back_to_one_categories():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="🔙назад", callback_data="back_one_categories")

    return keyboard.adjust().as_markup()