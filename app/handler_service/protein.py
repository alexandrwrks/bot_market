from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
<<<<<<< HEAD
from app.keyboards.categories import get_catalog_categories, get_protein_options
=======
from app.keyboards.categories import get_catalog_categories,  get_protein_options
>>>>>>> 953e1d2e5e35ac7d4bfdfa686317acb4f98bcf3d
from app.keyboards.Back import back_to_one
from app.keyboards.product import get_product_keyboard

from app.tests.db_test import TestProductTable

router = Router()


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
    
    for i in range(len(product)):
        name, description, price, photo_path = product[i]
        path = FSInputFile(photo_path)

        text = (
            f"{name}\n\n"
            f"{description}\n"
            f"Цена: {price} руб. за шт.\n"
        )

    await callback.message.answer_photo(
        photo=path,
        caption=text,
        reply_markup=get_product_keyboard()
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

# я что то добавил но временно
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_protein():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Банан-клубника", callback_data="protein:banana_strawberry")
    keyboard.button(text="Молочный шоколад", callback_data="protein:milk_chocolate")
    keyboard.button(text="Pina Colado", callback_data="protein:pina_colado")
    keyboard.button(text="🔙 Назад", callback_data="back_one_categories")
    return keyboard.adjust(2).as_markup()

def get_protein_options():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔄 Поменять вкус", callback_data="back_one")
    keyboard.button(text="🛒 В корзину", callback_data="add_to_cart")
    return keyboard.adjust(2).as_markup()