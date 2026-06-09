from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Product


def get_product_keyboard(slug: str, product_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="➕ Добавить в корзину", callback_data=f"basket:add:{product_id}"
    )
    keyboard.button(
        text="🔄 Выбрать другой вкус", callback_data=f"menu:catalog:category:{slug}"
    )
    keyboard.button(
        text="🔙 Вернуться к выбору категорий", callback_data="menu:catalog"
    )
    keyboard.button(text="🗑 Корзина", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()


def products_keyboard(products: list[Product], slug: str):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=f"{product.name}", callback_data=f"product:{slug}:{product.id}"
        )

    keyboard.button(text="🔙 Назад", callback_data="menu:catalog")

    return keyboard.adjust(1).as_markup()


def get_product_keyboard_before(slug: str):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="🔄 Выбрать другой вкус", callback_data=f"menu:catalog:category:{slug}"
    )
    keyboard.button(
        text="🔙 Вернуться к выбору категорий", callback_data="menu:catalog"
    )
    keyboard.button(text="🗑 Корзина", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()
