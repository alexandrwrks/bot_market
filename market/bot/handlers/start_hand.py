from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from market.bot.keyboards.start import get_start_inline_keyboard
from market.bot.service.user_service import user_service

router = Router()

WELCOME_TEXT = (
    "Добро пожаловать в SportMarketBot!\n"
    "Этот бот помогает покупать товары\n"
    "из каталога с доставкой.\n"
)


@router.message(Command("start"))
async def cmd_start_message(message: Message):
    await user_service.existing_user(message.from_user)  # → User

    await message.answer(
        text=WELCOME_TEXT,
        reply_markup=get_start_inline_keyboard(),
    )


@router.callback_query(F.data == "start_btn")
async def cmd_start_callback(callback: CallbackQuery):
    await callback.answer()
    keyboard = get_start_inline_keyboard()

    try:
        await callback.message.edit_text(
            text=WELCOME_TEXT,
            reply_markup=keyboard,
        )

    except Exception:
        await callback.message.delete()

        await callback.message.answer(
            text=WELCOME_TEXT,
            reply_markup=keyboard,
        )
