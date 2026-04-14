from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_catalog_company():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="PrimeKraft", callback_data="primekraft_btn")
    keyboard.button(text="Назад", callback_data="back_one_start")

    return keyboard.adjust(1).as_markup()
