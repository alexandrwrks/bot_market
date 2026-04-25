from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_catalog_categories():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Протеин", callback_data="protein_btn")
    keyboard.button(text="Гейнер", callback_data="geiner_btn")
    keyboard.button(text="Креатин", callback_data="creatin_btn")
    keyboard.button(text="БЦАА", callback_data="bcaa_btn")
    keyboard.button(text="Назад", callback_data="start_btn")

    return keyboard.adjust(1).as_markup()


def get_protein_options(products: list[tuple[int, str]]):
    keyboard = InlineKeyboardBuilder()

    for product_id, product_name in products:
        keyboard.button(text=product_name, callback_data=f"protein:{product_id}")

    keyboard.button(text="Назад", callback_data="back_one_categories")

    return keyboard.adjust(1).as_markup()


def get_categories_for_add_product():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Протеин", callback_data="add_category:protein")
    keyboard.button(text="Гейнер", callback_data="add_category:geiner")
    keyboard.button(text="Креатин", callback_data="add_category:creatin")
    keyboard.button(text="БЦАА", callback_data="add_category:bcaa")
    keyboard.button(text="Назад", callback_data="catalog_btn")

    return keyboard.adjust(2, 2, 1).as_markup()
