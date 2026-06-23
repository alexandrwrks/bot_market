from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.schema import ProductsInBasket


def get_keyboard_to_basket():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🔙 Корзина", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()


def get_user_basket():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="📦 Состав корзины", callback_data="basket:composition")
    keyboard.button(text="🧹 Очистить", callback_data="basket:clear")
    keyboard.button(text="📂 Каталог", callback_data="menu:catalog")
    keyboard.button(text="✅ Оформить заказ", callback_data="order:confirm")

    return keyboard.adjust(1, 2, 1).as_markup()


def get_user_basket_products(product: List[ProductsInBasket]):
    keyboard = InlineKeyboardBuilder()

    for product in product:
        text = f"{product.name} ({product.quantity} шт.)"
        keyboard.button(text=text, callback_data=f"basket:product:{product.product_id}")

    keyboard.button(text="🔙 Назад", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()


def change_basket_product_info(product_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➕ Добавить ещё", callback_data="menu:catalog")
    keyboard.button(
        text="❌ Удалить товар", callback_data=f"product:delete:{product_id}"
    )
    keyboard.button(text="🔙 Вернуться корзину", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()
