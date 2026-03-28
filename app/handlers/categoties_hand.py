from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from app.keyboards.categories import get_categories


router = Router()

@router.callback_query(F.data == "catalog_btn")
async def get_catalog(
    callback: CallbackQuery
):
    await callback.message.answer(
        text="Выберите категорию товара:",
        reply_markup=get_categories()
    )

    await callback.answer()
    
@router.callback_query(F.data == "protein_btn")
async def get_test_protein(
    callback: CallbackQuery
):
    images = FSInputFile("images\protein\primekraft_protein_banana_strawberry.jpg")
    text = ("Протени PrimeKraft со вкусом банана и клубники\n"
            "Стоимость: 400 рублей за 1 шт.")

    await callback.message.answer_photo(
        photo=images,
        caption=text
    )

    await callback.answer()