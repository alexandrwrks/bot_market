from aiogram.utils.keyboard import InlineKeyboardBuilder

from market.database.models import Product


def get_exists_catalog_for_admin(existing_categories):
    keyboard = InlineKeyboardBuilder()

    for category in existing_categories:
        keyboard.button(
            text=category.name, callback_data=f"admin_category:{category.slug}"
        )

    keyboard.button(text="🔙 Назад", callback_data="back_to_admin")

    return keyboard.adjust(1).as_markup()


def get_admin_products_keyboard(products: list[Product], slug: str):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=f"{product.name}", callback_data=f"admin_product:{slug}:{product.id}"
        )

    keyboard.button(text="🔙 Назад", callback_data="admin_update_products")

    return keyboard.adjust(1).as_markup()


def get_options_for_changes(slug: str, product_id: int):
    keyboard = InlineKeyboardBuilder()
    """
        Выбор изменений: 
    цена, количество, фото, описание, удаление товара(мягкое),
    """
    keyboard.button(
        text="Изменить цену товара", callback_data=f"price_change:{slug}:{product_id}"
    )
    keyboard.button(
        text="Изменить количество", callback_data=f"quantity_change:{slug}:{product_id}"
    )
    keyboard.button(text="Изменить фото", callback_data=f"photo_change:{slug}:{product_id}")
    keyboard.button(
        text="Изменить описание", callback_data=f"description_change:{slug}:{product_id}"
    )
    keyboard.button(
        text="❌ Мягкое удаление товара", callback_data=f"delete_change:{slug}:{product_id}"
    )

    keyboard.button(
        text="🔄 Выбрать другой вкус", callback_data=f"admin_category:{slug}"
    )
    keyboard.button(
        text="🔙 Вернуться к категориям", callback_data="admin_update_products"
    )

    return keyboard.adjust(1, 1, 1, 1, 1, 2).as_markup()


def get_access_options():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Отменить", callback_data="delete_price_change")
    keyboard.button(text="Продолжить", callback_data="access_price_change")

    return keyboard.adjust(1).as_markup()

def get_access_options_quantity():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Отменить", callback_data="delete_quantity_change")
    keyboard.button(text="Продолжить", callback_data="access_quantity_change")

    return keyboard.adjust(1).as_markup()