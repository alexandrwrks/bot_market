from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.start import get_start_inline_keyboard
from app.keyboards.company import get_catalog_company
from app.keyboards.categories import get_catalog_categories

router = Router()

@router.callback_query(F.data == "back_one_start")
async def back_to_start_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer(
        text="Главное меню:",
        reply_markup=get_start_inline_keyboard()
        )
    
@router.callback_query(F.data == "back_one_company")
async def back_to_company_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer(
        text="Выберите компанию:",
        reply_markup=get_catalog_company()
        )
    
@router.callback_query(F.data == "back_one_categories")
async def back_to_categories_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer(
        text="Выберите категорию: ",
        reply_markup=get_catalog_categories()
        )