from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.Back import back_to_one_start
from app.keyboards.start import get_start_inline_keyboard

router = Router()

def get_catalog_company():

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="PrimeKraft", callback_data="primekraft_btn")
    # keyboard.button(text="Mutant", callback_data="mutant_btn")
    # keyboard.button(text="Maxler", callback_data="maxler_btn")
    # keyboard.button(text="Dr.Hoffman", callback_data="hoffman_btn")
    keyboard.button(text="🔙 Назад", callback_data="back_one_start")

    return keyboard.adjust(1).as_markup()

@router.callback_query(F.data == "back_one_start")
async def back_to_start_handler(
    callback: CallbackQuery
):
    await callback.answer()

    await callback.message.edit_text(
        text = ("Добро пожаловать в SportMarketBot!\n"
           "Этот бот позволяет приобрести товары\n"
           "из каталога с доставкой по всей Росии.\n"),
        reply_markup=get_start_inline_keyboard()
        )