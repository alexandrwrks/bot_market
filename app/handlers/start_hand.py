from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards.start import get_start_inline_keyboard




router = Router()

@router.message(Command("start"))
async def cmd_start(
    message: Message
):
    text = ("Добро пожаловать в SportMarketBot!\n"
           "Этот бот позволяет приобрести товары\n"
           "из каталога с доставкой по всей Росии.\n")
    
    await message.answer(
        text=text,
        reply_markup=get_start_inline_keyboard()
    )




