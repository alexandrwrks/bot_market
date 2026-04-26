from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_one():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Поменять вкус", callback_data="back_one")
    return keyboard.as_markup()


def put_it_inside():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="В корзину", callback_data="")
    return keyboard.as_markup()


def back_to_one_start():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="back_one_start")
    return keyboard.as_markup()


def back_to_one_company():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="back_one_company")
    return keyboard.as_markup()


def back_to_one_categories():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="back_one_categories")
    return keyboard.as_markup()
