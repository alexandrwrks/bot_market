from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from market.database.models import Product


def get_product_keyboard(slug: str, product_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➕ Добавить в корзину", callback_data=f"add_to_cart:{product_id}")
    keyboard.button(text="🔄 Выбрать другой вкус", callback_data=f"category:{slug}")
    keyboard.button(text="🔙 Вернуться к выбору категорий", callback_data="catalog_btn")
    keyboard.button(text="🗑 Корзина", callback_data="basket_btn")

    return keyboard.adjust(1).as_markup()


def products_keyboard(products: list[Product], slug: str):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=f"{product.name}", callback_data=f"product:{slug}:{product.id}"
        )

    keyboard.button(text="🔙 Назад", callback_data="catalog_btn")

    return keyboard.adjust(1).as_markup()


def get_product_keyboard_before(slug: str):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🔄 Выбрать другой вкус", callback_data=f"category:{slug}")
    keyboard.button(text="🔙 Вернуться к выбору категорий", callback_data="catalog_btn")
    keyboard.button(text="🗑 Корзина", callback_data="basket_btn")

    return keyboard.adjust(1).as_markup()


def get_admin_products_keyboard(products: list[Product], slug: str):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=f"{product.name}", callback_data=f"admin_product:{slug}:{product.id}"
        )

    keyboard.button(text="🔙 Назад", callback_data="admin_category")

    return keyboard.adjust(1).as_markup()

def get_options_for_changes(slug:str, product_id: int):
    keyboard = InlineKeyboardBuilder()
    """
        Выбор изменений: 
    цена, количество, фото, описание, удаление товара(мягкое),
    """
    keyboard.button(text="Изменить цену товара", callback_data=f"price_change:{product_id}")
    keyboard.button(text="Изменить количество", callback_data=f"quantity_change:{product_id}")
    keyboard.button(text="Изменить фото", callback_data=f"photo_change:{product_id}")
    keyboard.button(text="Изменить описание", callback_data=f"description_change:{product_id}")
    keyboard.button(text="❌ Мягкое удаление товара", callback_data=f"delete_change:{product_id}")

    keyboard.button(text="🔄 Выбрать другой вкус", callback_data=f"admin_product:{slug}")
    keyboard.button(text="🔙 Вернуться к выбору категорий", callback_data="admin_category")

    return keyboard.adjust(1, 1, 1, 1, 1, 2).as_markup()