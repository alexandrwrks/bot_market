import asyncio

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.repo.categories import categories_repo
from app.database.models import Category

async def get_categories_from_repo():
    existing_categories = await categories_repo.get_existing_categories()
    return get_exists_catalog(existing_categories)

def get_exists_catalog(existing_categories: list[Category]):
    keyboard = InlineKeyboardBuilder()

    for category in existing_categories:
        keyboard.button(
            text=category.name,
            callback_data=f"category:{category.slug}"
        )
        print(f"text={category.name}\ncallback_data=category:{category.slug}")
    
    # Кнопка назад -> Стартовая точка
    keyboard.button(text="Назад", callback_data="start_btn")

    return keyboard.adjust(1).as_markup()

if __name__ == "__main__":
    asyncio.run(get_categories_from_repo())