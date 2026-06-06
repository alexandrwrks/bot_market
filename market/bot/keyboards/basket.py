from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

from market.schemas.schema import ProductsInBasket


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

    keyboard.button(text="Назад", callback_data="menu:basket")

    return keyboard.adjust(1).as_markup()


def checkout_kb(profile: dict):
    has_address = bool(profile.get("address_value"))
    has_name = bool(profile.get("recipient_full_name"))
    has_phone = bool(profile.get("phone_number"))

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=("✏ Изменить адрес" if has_address else "➕ Ввести адрес"),
        callback_data="checkout:address",
    )

    keyboard.button(
        text=("✏ Изменить ФИО" if has_name else "➕ Ввести ФИО"),
        callback_data="checkout:name",
    )

    keyboard.button(
        text=("✏ Изменить телефон" if has_phone else "➕ Ввести телефон"),
        callback_data="checkout:phone",
    )

    keyboard.button(text="⬅ Назад", callback_data="menu:basket")
    keyboard.button(text="📂 Каталог", callback_data="menu:catalog")
    keyboard.button(text="✅ Подтвердить", callback_data="order:verify")

    return keyboard.adjust(1, 1, 1, 2, 1).as_markup()
