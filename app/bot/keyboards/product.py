from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_product_keyboard(product_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Добавить в корзину", callback_data=f"add_to_cart:{product_id}")
    keyboard.button(text="Выбрать другой вкус", callback_data="back_to_protein_list")
    keyboard.button(text="Вернуться в категории", callback_data="back_one_categories")
    keyboard.button(text="Корзина", callback_data="basket_btn")

    return keyboard.adjust(1).as_markup()
