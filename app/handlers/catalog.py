from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.keyboards.categories import get_categories_from_repo
from app.repo.categories import categories_repo
from app.repo.products import product_repo

router = Router()


@router.callback_query(F.data == "catalog_btn")
async def get_categories_of_catalog(callback: CallbackQuery):
    await callback.answer()

    categories = await categories_repo.get_existing_categories()
    if not categories:
        await callback.message.answer("Сейчас нет доступных категорий.")
    else:
        try:
            await callback.message.edit_text(
                text="Выберите категорию:",
                reply_markup=await get_categories_from_repo(),
            )
        except Exception:
            await callback.message.answer(
                text="Выберите категорию:",
                reply_markup=await get_categories_from_repo(),
            )



@router.message(Command("catalog"))
async def get_exists_category(message: Message):
    await message.answer(
        text="Выберите категорию:",
        reply_markup=await get_categories_from_repo()
    )


