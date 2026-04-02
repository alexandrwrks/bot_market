from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from app.keyboards.categories import get_catalog_categories
from app.keyboards.company import get_catalog_company
from app.handler_service.protein import router as protein_router

router = Router()
router.include_router(protein_router)

@router.callback_query(F.data == "catalog_btn")
async def get_catalog(
    callback: CallbackQuery
):
    await callback.message.edit_text(
        text="Выберите компанию:",
        reply_markup=get_catalog_company()
    )

    await callback.answer()
    

@router.callback_query(F.data == "primekraft_btn")
async def get_categories_of_catalog(
    callback: CallbackQuery
):
    await callback.message.edit_text(
        text="Выберите категорию: ",
        reply_markup=get_catalog_categories()
    )
    
    await callback.answer()