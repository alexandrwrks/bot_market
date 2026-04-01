from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from app.keyboards.categories import get_catalog_categories, get_protein, get_protein_options
from app.keyboards.Back import back_to_one

from tests.db_test import TestProductTable

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
async def show_protein_tastes(
    callback: CallbackQuery
):
    tpt = TestProductTable()

    products = await tpt.get_product_names_by_category_id(1)
    
    await callback.message.edit_text(
        text="Выберите вкус:",
        reply_markup=get_protein_options(products)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("protein:"))
async def protein_selected(callback: CallbackQuery):
    await callback.answer()

    protein_id = int(callback.data.split(":")[1])

    tpt = TestProductTable()
    product = await tpt.get_product_by_id(protein_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return
    
    name, description, price, photo_path, quantity = product
    path = FSInputFile(photo_path)

    text = (
        f"{name}\n\n"
        f"{description}\n"
        f"Цена: {price} руб.\n"
        f"В наличии: {quantity}"
    )

    await callback.message.answer_photo(
        photo=path,
        caption=text
    )

    

@router.callback_query(F.data == "back_one_category")
async def back_to_categories_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer(
        text="Выберите категорию: ",
        reply_markup=get_catalog_categories()
        )

@router.callback_query(F.data == "back_one")
async def back_to_protein_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.answer(
        text="Выберите вкус:",
        reply_markup=get_protein()
    )