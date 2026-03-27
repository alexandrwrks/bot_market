from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(
    message: Message
):
    text = """
    Добро пожаловать в SportMarketBot!\n
    Этот бот позволяет приобрести товары\n
    из каталога с доставкой по всей Росии.\n
"""
    await message.answer(
        text=text,
        # reply_markup=
    )