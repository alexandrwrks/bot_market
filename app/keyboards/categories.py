from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_catalog_categories():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Протеин", callback_data="protein_btn")
    # keyboard.button(text="Гейнер", callback_data="geiner_btn")
    # keyboard.button(text="Креатин", callback_data="creatin_btn")
    # keyboard.button(text="BCAA", callback_data="bcaa_btn")

    return keyboard.adjust(1).as_markup()

def get_protein():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Банан-клубника", callback_data="protein:banana_strawberry")
    keyboard.button(text="Молочный шоколад", callback_data="protein:milk_chocolate")
    keyboard.button(text="Pina Colado", callback_data="protein:pina_colado")

    return keyboard.adjust(2).as_markup()
