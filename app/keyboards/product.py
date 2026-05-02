from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Product


def get_product_keyboard(product_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Добавить в корзину", callback_data=f"add_to_cart:{product_id}")
    keyboard.button(text="Выбрать другой вкус", callback_data="taste_btn")
    keyboard.button(text="Выбрать другую категорию", callback_data="catalog_btn")
    keyboard.button(text="Корзина", callback_data="basket_btn")
     
    return keyboard.adjust(1).as_markup()

def products_keyboard(products: list[Product]):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=f"{product.name}",
            callback_data=f"product:{product.id}"
        )

    keyboard.button(text="Назад", callback_data="catalog_btn")

    return keyboard.adjust(1).as_markup()


