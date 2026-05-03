from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.repo.categories import categories_repo
from app.database.models import Category


# Система для вывода категорий имеющих хотя-бы один товар
async def get_categories_from_repo():
    existing_categories = await categories_repo.get_existing_categories()
    return get_exists_catalog(existing_categories)

def get_exists_catalog(existing_categories: list[Category]):
    """Выводим каталог категорий с теми где есть хотя-бы один товар"""
    keyboard = InlineKeyboardBuilder()

    # С помощью цикла создаем клавиатуру категорий
    for category in existing_categories:
        keyboard.button(
            text=category.name,
            callback_data=f"category:{category.slug}"
        )
    
    # Кнопка назад -> Стартовая точка
    keyboard.button(text="Назад", callback_data="start_btn")

    # Возращаем клавиатуру
    return keyboard.adjust(1).as_markup()