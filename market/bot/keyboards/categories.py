from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_exists_catalog(existing_categories):
    """Выводим каталог категорий с теми где есть хотя-бы один товар"""
    keyboard = InlineKeyboardBuilder()

    # С помощью цикла создаем клавиатуру категорий
    for category in existing_categories:
        keyboard.button(text=category.name, callback_data=f"category:{category.slug}")

    # Кнопка назад -> Стартовая точка
    keyboard.button(text="🔙 Назад", callback_data="start_btn")

    # Возращаем клавиатуру
    return keyboard.adjust(1).as_markup()


def get_exists_catalog_for_admin(existing_categories):
    keyboard = InlineKeyboardBuilder()

    for category in existing_categories:
        keyboard.button(text=category.name, callback_data=f"admin_category:{category.slug}")

    keyboard.button(text="🔙 Назад", callback_data="back_to_admin")

    return keyboard.adjust(1).as_markup()