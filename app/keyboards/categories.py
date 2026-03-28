from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_categories():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Протеин", callback_data="protein_btn")
    keyboard.button(text="Гейнер", callback_data="geiner_btn")
    keyboard.button(text="Креатин", callback_data="creatin_btn")
    keyboard.button(text="BCAA", callback_data="bcaa_btn")

    return keyboard.adjust(1).as_markup()