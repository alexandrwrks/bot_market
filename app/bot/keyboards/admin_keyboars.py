from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Category


def get_back_admin_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🔙 Вернуться в главное меню", callback_data="admin_panel:menu")

    return keyboard.adjust(1).as_markup()


def get_admin_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➕ Добавить товары", callback_data="admin_panel:products:add")
    keyboard.button(text="➕ Категории", callback_data="admin_panel:category")
    keyboard.button(
        text="🔄 Обновить товары", callback_data="admin_panel:products:update"
    )
    keyboard.button(
        text="📈 Посмотреть заказы", callback_data="admin_admin:orders:view"
    )
    keyboard.button(
        text="📊 Посмотреть статистику", callback_data="admin_admin:statistics:view"
    )

    return keyboard.adjust(1).as_markup()

def access_product_delete(slug: str, product_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="❌ Отменить удаление", callback_data=f"admin_panel:product:delete:{slug}:{product_id}:cancel")
    keyboard.button(text="✅ Подтвердить удаление", callback_data=f"admin_panel:product:delete:{slug}:{product_id}:confirm")

    return keyboard.adjust(1).as_markup()

def get_catalog_for_admin(categories: List[Category]):
    keyboard = InlineKeyboardBuilder()

    for category in categories:
        if category.is_active:
            keyboard.button(
                text=f"{category.name} (✅ Активна)",
                callback_data=f"admin_panel:products:add:{category.id}"
            )

        else:
            keyboard.button(
                text=f"{category.name} (❌ Не активна)",
                callback_data=f"admin_panel:products:add:{category.id}"
            )

    return keyboard.adjust(1).as_markup()

def get_access_add_product():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="❌ Отменить", callback_data="admin_panel:products:add_confirmation:cancel")
    keyboard.button(text="✅ Добавить", callback_data="admin_panel:products:add_confirmation:confirm")

    return keyboard.adjust(1).as_markup()

def get_categories_keyboard(categories: List[Category]):
    keyboard = InlineKeyboardBuilder()

    for category in categories:
        if category.is_active:
            keyboard.button(
                text=f"{category.name} (✅ Активна)",
                callback_data=f"admin_panel:category:toggle:{category.id}")

        else:
            keyboard.button(
                text=f"{category.name} (❌ Не активна)",
                callback_data=f"admin_panel:category:toggle:{category.id}"
            )

    keyboard.button(text="➕ Добавить категорию", callback_data="admin_panel:category:add")
    keyboard.button(text="🔙 Главное меню", callback_data="admin_panel:menu")

    return keyboard.adjust(1).as_markup()

def access_add_new_category():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="❌ Отмена", callback_data="admin_panel:category_add:cancel")
    keyboard.button(text="✅ Добавить", callback_data="admin_panel:category_add:confirm")

    return keyboard.adjust(1).as_markup()