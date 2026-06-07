from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.exception.category_ex import NotCategoryError
from app.bot.keyboards.categories import get_exists_catalog
from app.bot.service.category_service import category_service

router = Router()


@router.callback_query(F.data == "menu:catalog")
async def get_categories_of_catalog(callback: CallbackQuery):
    try:
        categories = await category_service.get_categories()

        keyboard = get_exists_catalog(categories)

        await callback.answer()
        try:
            await callback.message.edit_text(
                text="Выберите категорию:",
                reply_markup=keyboard,
            )

        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                text="Выберите категорию:",
                reply_markup=keyboard,
            )

    except NotCategoryError:
        await callback.answer(
            text="Сейчас нет доступных категорий.",
            show_alert=True,
        )


@router.message(Command("catalog"))
async def get_exists_category(message: Message):
    try:
        categories = await category_service.get_categories()

        keyboard = get_exists_catalog(categories)

        await message.answer(text="Выберите категорию:", reply_markup=keyboard)

    except NotCategoryError:
        await message.answer("Сейчас нет доступных категорий")
        return
