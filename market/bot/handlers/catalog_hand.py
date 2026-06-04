from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from market.bot.exception.category_ex import NotCategoryError
from market.bot.keyboards.categories import get_exists_catalog
from market.bot.service.category_service import category_service

router = Router()


@router.callback_query(F.data == "catalog_btn")
async def get_categories_of_catalog(callback: CallbackQuery):
    try:
        categories = await category_service.get_categories()

        keyboard = get_exists_catalog(categories)


        try:
            await callback.answer()
            await callback.message.edit_text(
                text="Выберите категорию:",
                reply_markup=keyboard,
            )

        except TelegramBadRequest:
            await callback.answer()
            
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
