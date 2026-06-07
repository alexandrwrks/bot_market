from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Product


def get_exists_catalog_for_admin(existing_categories):
    keyboard = InlineKeyboardBuilder()

    for category in existing_categories:
        keyboard.button(
            text=category.name,
            callback_data=f"admin_panel:catalog:category:{category.slug}",
        )

    keyboard.button(text="🔙 Назад", callback_data="admin_panel:menu")

    return keyboard.adjust(1).as_markup()


def get_admin_products_keyboard(products: list[Product], slug: str):
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=f"{product.name}",
            callback_data=f"admin_panel:catalog:products:{slug}:{product.id}",
        )

    keyboard.button(text="🔙 Назад", callback_data="admin_panel:products:update")

    return keyboard.adjust(1).as_markup()


def get_options_for_changes(slug: str, product_id: int):
    keyboard = InlineKeyboardBuilder()
    """
        Выбор изменений: 
    цена, количество, фото, описание, удаление товара(мягкое),
    """
    keyboard.button(
        text="Изменить цену товара",
        callback_data=f"admin_panel:change:price:{slug}:{product_id}",
    )
    keyboard.button(
        text="Изменить количество",
        callback_data=f"admin_panel:change:quantity:{slug}:{product_id}",
    )
    keyboard.button(
        text="Изменить фото",
        callback_data=f"admin_panel:change:photo:{slug}:{product_id}",
    )
    keyboard.button(
        text="Изменить описание",
        callback_data=f"admin_panel:change:description:{slug}:{product_id}",
    )
    keyboard.button(
        text="❌ Мягкое удаление товара",
        callback_data=f"admin_panel:change:delete:{slug}:{product_id}",
    )

    keyboard.button(
        text="🔄 Выбрать другой вкус",
        callback_data=f"admin_panel:catalog:category:{slug}",
    )
    keyboard.button(
        text="🔙 Вернуться к категориям", callback_data="admin_panel:products:update"
    )

    return keyboard.adjust(1, 1, 1, 1, 1, 2).as_markup()


def get_access_options():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Отменить", callback_data="change:delete_price")
    keyboard.button(text="Продолжить", callback_data="change:access_price")

    return keyboard.adjust(1).as_markup()


def get_access_options_quantity():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Отменить", callback_data="change:delete_quantity")
    keyboard.button(text="Продолжить", callback_data="change:access_quantity")

    return keyboard.adjust(1).as_markup()
