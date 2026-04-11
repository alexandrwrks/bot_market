from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from app.keyboards.start import get_start_inline_keyboard
from app.db_repo.users import user_repo
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

    user_exists = await user_repo.exists_user_by_telegram_id(tg_user.id)

    if user_exists is None:
        await user_repo.create_user(tg_user)





