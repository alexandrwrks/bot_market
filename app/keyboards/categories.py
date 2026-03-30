from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards.company import get_catalog_company

router = Router()

def get_catalog_categories():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Протеин", callback_data="protein_btn")
    # keyboard.button(text="Гейнер", callback_data="geiner_btn")
    # keyboard.button(text="Креатин", callback_data="creatin_btn")
    # keyboard.button(text="BCAA", callback_data="bcaa_btn")
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
    

    
def get_protein():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Банан-клубника", callback_data="protein:banana_strawberry")
    keyboard.button(text="Молочный шоколад", callback_data="protein:milk_chocolate")
    keyboard.button(text="Pina Colado", callback_data="protein:pina_colado")
    keyboard.button(text="🔙 Назад", callback_data="back_one_categories")

    return keyboard.adjust(2, 1, 1).as_markup()