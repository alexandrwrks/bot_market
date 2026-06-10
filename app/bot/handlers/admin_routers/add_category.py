from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.fsm.fsms import AddNewCategory
from app.bot.keyboards.admin_keyboars import (access_add_new_category,
                                              get_back_admin_keyboard,
                                              get_categories_keyboard)
from app.bot.service.admin_service import admin_service
from app.bot.service.category_service import category_service
from app.utils import logger

router = Router()

@router.callback_query(F.data == "admin_panel:category")
async def add_category(callback: CallbackQuery):
    try:
        """
        TODO: Получаем все категории и делаем кнопки для каждой из них,
        если категория активна → ✅ Активна, если категория не активна → ❌ Не активна
        Пользователь с помощью нажатий сам выбирает что включить, а что отключить,
        если была "активна", то станет "не активна" и наоборот
        Снизу будет кнопка для того чтобы добавить новую категорию → ➕ Добавить новую категорию
        
        
        FSM для добавления новой категории: name: str, slug: str(название на английском), description: str
        """
        categories= await category_service.get_categories_for_admin()

        await callback.message.edit_text(
            text="📱 Выберите действие",
            reply_markup=get_categories_keyboard(categories)
        )

    except Exception as e:
        logger.error("Ошибка отработки хэндлера для показа доступных категорий %s", e)
        await callback.answer(text="❌ Ошибка выдачи категорий. Попробуйте позже.")
        return

@router.callback_query(F.data.startswith("admin_panel:category:toggle:"))
async def admin_panel_category_toggle(callback: CallbackQuery):
    try:
        category_id = int(callback.data.split(":")[-1])

        await category_service.update_category(category_id)

        categories= await category_service.get_categories_for_admin()

        await callback.message.edit_reply_markup(
            reply_markup=get_categories_keyboard(categories)
        )

    except Exception:
        await callback.answer(
            text="❌ Ошибка изменения статуса категории",
            show_alert=True
        )
        return

@router.callback_query(F.data == "admin_panel:category:add")
async def admin_panel_category_add(callback: CallbackQuery, state: FSMContext):
    try:
        await state.set_state(AddNewCategory.name)

        await callback.answer()
        await callback.message.edit_text("Введите название для новой категории:")

    except Exception as e:
        logger.error("Ошибка добавления нового товара %s", e)

        await callback.answer(
            text="❌ Ошибка добавления нового товара",
            show_alert=True
        )
        return

@router.message(AddNewCategory.name)
async def process_name_category(message: Message, state: FSMContext):
    name = message.text

    await state.update_data(name=name)

    await state.set_state(AddNewCategory.slug)
    await message.answer("Введите slug для новой категорию")

@router.message(AddNewCategory.slug)
async def process_name_category(message: Message, state: FSMContext):
    try:
        slug = message.text
        await state.update_data(slug=slug)

        data = await state.get_data()

        text = (
            "Новая категория:\n\n"
            f"Название: {data['name']}\n"
            f"Slug: {data['slug']}\n"
        )

        await message.answer(text)

        await message.answer(
            text="📱 Выберите действие:",
            reply_markup=access_add_new_category()
        )

    except Exception:
        await message.answer(
            text="❌ Ошибка обработки добавления категории",
            reply_markup=get_back_admin_keyboard()
        )
        return


@router.callback_query(F.data.startswith("admin_panel:category_add:"))
async def add_new_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    try:
        action = callback.data.split(":")[-1]

        if action == "cancel":
            await state.clear()

            await callback.message.edit_text(
                text="✖️ Отмена добавления новой категории",
                reply_markup=get_back_admin_keyboard()
            )

        else:
            data = await state.get_data()

            await admin_service.add_new_category(data)

            await callback.message.edit_text(
                text=f"✅ Успешное добавления новой категории: {data['name']}",
                reply_markup=get_back_admin_keyboard()
            )


    except Exception as e:
        logger.error("Ошибка добавления новой категории %s", e)

        await callback.message.edit_text(
            text="❌ Ошибка добавления категории",
            reply_markup=get_back_admin_keyboard()
        )