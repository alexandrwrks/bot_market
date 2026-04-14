from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.db_repo.users import user_repo
from app.keyboards.start import get_start_inline_keyboard

router = Router()

WELCOME_TEXT = (
    "Добро пожаловать в SportMarketBot!\n"
    "Этот бот помогает покупать товары\n"
    "из каталога с доставкой.\n"
)


@router.message(Command("start"))
async def cmd_start_message(message: Message):
    tg_user = message.from_user

    await message.answer(
        text=WELCOME_TEXT,
        reply_markup=get_start_inline_keyboard(),
    )

    user_exists = await user_repo.exists_user_by_telegram_id(tg_user.id)
    if user_exists is None:
        await user_repo.create_user(tg_user)


@router.callback_query(F.data == "start_btn")
async def cmd_start_callback(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text=WELCOME_TEXT,
        reply_markup=get_start_inline_keyboard(),
    )
