from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.repo.categories import categories_repo
from app.database.models import Category


def get_products_optinios(callback: CallbackQuery):
    """
    1. Создать клавитуру для товаров по той категории которую выберит пользователь
    2. Выдать клавиатуру пользователю

    План: 
    Получаем категорию которую выбрал пользоватлеь после чего создаём callback-и для каждого товара с помощью цифр ->
    product:0, product:1 и тд
    """


    keyboard = InlineKeyboardBuilder()

    return ...

def get_protein_options(products: list[tuple[int, str]]):
    keyboard = InlineKeyboardBuilder()

    for product_id, product_name in products:
        keyboard.button(text=product_name, callback_data=f"protein:{product_id}")

    keyboard.button(text="Назад", callback_data="back_one_categories")

    return keyboard.adjust(1).as_markup()

# Система для вывода категорий имеющих хотя-бы один товар
async def get_categories_from_repo():
    existing_categories = await categories_repo.get_existing_categories()
    return get_exists_catalog(existing_categories)

def get_exists_catalog(existing_categories: list[Category]):
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