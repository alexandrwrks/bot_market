from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.categories import get_catalog_categories
from app.bot.keyboards.company import get_catalog_company
from app.bot.keyboards.start import get_start_inline_keyboard

router = Router()

WELCOME_TEXT = (
    "Добро пожаловать в SportMarketBot!\n"
    "Этот бот помогает покупать товары\n"
    "из каталога с доставкой.\n"
)


@router.callback_query(F.data == "back_one_start")
async def back_to_start_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=WELCOME_TEXT,
        reply_markup=get_start_inline_keyboard(),
    )


@router.callback_query(F.data == "back_one_company")
async def back_to_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="Выберите компанию:",
        reply_markup=get_catalog_company(),
    )


@router.callback_query(F.data == "back_one_categories")
async def back_to_categories_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="Выберите категорию:",
        reply_markup=get_catalog_categories(),
    )
