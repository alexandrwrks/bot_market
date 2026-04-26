from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.repo.users import user_repo
from app.keyboards.start import get_start_inline_keyboard

router = Router()

WELCOME_TEXT = (
    "Добро пожаловать в SportMarketBot!\n"
    "Этот бот помогает покупать товары\n"
    "из каталога с доставкой.\n"
)


@router.message(Command("start"))
async def cmd_start_message(message: Message):
    telegram_id = message.from_user.id
    await user_repo.get_or_create_user(telegram_id)

    await message.answer(
        text=WELCOME_TEXT,
        reply_markup=get_start_inline_keyboard(),
    )

@router.callback_query(F.data == "start_btn")
async def cmd_start_callback(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text=WELCOME_TEXT,
        reply_markup=get_start_inline_keyboard(),
    )
