from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards.company import get_catalog_company

router = Router()

def get_catalog_categories():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Протеин", callback_data="protein_btn")
    keyboard.button(text="Гейнер", callback_data="geiner_btn")
    keyboard.button(text="Креатин", callback_data="creatin_btn")
    keyboard.button(text="BCAA", callback_data="bcaa_btn")
    keyboard.button(text="🔙 Назад", callback_data="back_one_company")

    return keyboard.adjust(1).as_markup()

@router.callback_query(F.data == "back_one_company")
async def back_to_company_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.edit_text(
        text="Выберите компанию:",
        reply_markup=get_catalog_company()
        )
    

def get_protein_options(products: list[tuple]):
    keyboard = InlineKeyboardBuilder()

    for product_id, product_name in products:
        keyboard.button(
            text=product_name,
            callback_data=f"protein:{product_id}"
        )

    keyboard.button(text="🔙 Назад", callback_data="back_one_categories")

    return keyboard.adjust(1).as_markup()