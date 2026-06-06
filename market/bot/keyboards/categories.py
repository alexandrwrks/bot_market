from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_exists_catalog(existing_categories):
    """Выводим каталог категорий с теми где есть хотя-бы один товар"""
    keyboard = InlineKeyboardBuilder()

    # С помощью цикла создаем клавиатуру категорий
    for category in existing_categories:
        keyboard.button(text=category.name, callback_data=f"menu:catalog:category:{category.slug}")

    # Кнопка назад -> Стартовая точка
    keyboard.button(text="🔙 Назад", callback_data="start")

    # Возращаем клавиатуру
    return keyboard.adjust(1).as_markup()
