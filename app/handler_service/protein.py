from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from app.keyboards.categories import get_protein

router = Router()

PRODUCTS = {
    "banana_strawberry": {
        "image": "images/protein/primekraft_protein_banana_strawberry_900.jpg",
        "text": "Протеин PrimeKraft\nВкус: Банан-клубника\nЦена: 400 рублей"
    },
    "milk_chocolate": {
        "image": "images/protein/primekraft_protein_chocolate_900.jpg",
        "text": "Протеин PrimeKraft\nВкус: Молочный шоколад\nЦена: 420 рублей"
    },
    "pina_colado": {
        "image": "images/protein/primekraft_protein_pina_colado_900.jpg",
        "text": "Протени PrimeKraft\nВкус: Пина Коладо\nЦена: 410 рублей"
    }
}


@router.callback_query(F.data == "protein_btn")
async def get_categories_protein_keyboards(
    callback: CallbackQuery
):
    await callback.answer()
    
    await callback.message.answer(
        text="Выберите вкус:",
        reply_markup=get_protein()
    )


@router.callback_query(F.data == "protein:banana_strawberry")
async def protein_banana_strawberry(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer_photo(
        photo=FSInputFile(PRODUCTS["banana_strawberry"]["image"]),
        caption=PRODUCTS["banana_strawberry"]["text"]
    )


@router.callback_query(F.data == "protein:milk_chocolate")
async def protein_milk_chocolate(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer_photo(
        photo=FSInputFile(PRODUCTS["milk_chocolate"]["image"]),
        caption=PRODUCTS["milk_chocolate"]["text"]
    )


@router.callback_query(F.data == "protein:pina_colado")
async def protein_pina_colado_protein(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer_photo(
        photo=FSInputFile(PRODUCTS["pina_colado"]["image"]),
        caption=PRODUCTS["pina_colado"]["text"]
    )
