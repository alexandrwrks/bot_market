from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_catalog_company():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="PrimeKraft", callback_data="primekraft_btn")
    # keyboard.button(text="Mutant", callback_data="mutant_btn")
    # keyboard.button(text="Maxler", callback_data="maxler_btn")
    # keyboard.button(text="Dr.Hoffman", callback_data="hoffman_btn")

    return keyboard.adjust(1).as_markup()