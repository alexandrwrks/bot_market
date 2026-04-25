from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.categories import get_catalog_categories

router = Router()


@router.callback_query(F.data == "catalog_btn")
async def get_categories_of_catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите категорию:",
        reply_markup=get_catalog_categories(),
    )
    await callback.answer()


@router.callback_query(F.data.in_({"geiner_btn", "creatin_btn", "bcaa_btn"}))
async def not_ready_categories(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Эта категория в разработке. Сейчас доступен только раздел 'Протеин'.")
