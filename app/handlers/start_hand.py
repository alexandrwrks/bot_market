from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards.start import get_start_inline_keyboard
from app.models.users_db import users_manager



router = Router()

@router.message(Command("start"))
async def cmd_start(
    message: Message
):  
    tg_user = message.from_user

    text = ("Добро пожаловать в SportMarketBot!\n"
           "Этот бот позволяет приобрести товары\n"
           "из каталога с доставкой по всей Росии.\n")
    
    await message.answer(
        text=text,
        reply_markup=get_start_inline_keyboard()
    )

    user_exists = await users_manager.exists_user_by_telegram_id(tg_user.id)


    if not user_exists:
        await users_manager.create_user(tg_user)





