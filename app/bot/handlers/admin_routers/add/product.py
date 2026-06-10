import uuid
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.bot.fsm.fsms import AddNewProduct
from app.bot.keyboards.admin_keyboars import (get_access_add_product,
                                              get_back_admin_keyboard,
                                              get_catalog_for_admin)
from app.bot.service.admin_service import admin_service
from app.bot.service.category_service import category_service
from app.utils import logger

IMAGES_DIR = Path('images/products')
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

router = Router()

@router.callback_query(F.data == "admin_panel:products:add")
async def admin_products_callback(callback: CallbackQuery):
    """
    Добавить FSM для добавления товара:
    1) выбор категории
    2) FSM для написания данных о товаре
    3) подтверждение добавления товара
    """
    try:
        categories = await admin_service.get_admin_categories()

        await callback.answer()
        await callback.message.edit_text(
            text="📱 Выберите категорию",
            reply_markup=get_catalog_for_admin(categories)
        )

    except Exception:
        logger.error("Ошибка добавления товара")

        await callback.answer("❌ Ошибка получения категорий. Попробуйте позже")
        return

@router.callback_query(F.data.startswith("admin_panel:products:add:"))
async def admin_panel_product_add(callback: CallbackQuery, state: FSMContext):
    try:
        category_id = int(callback.data.split(":")[-1])

        await state.update_data(category_id=category_id)
        await state.set_state(AddNewProduct.name)

        await callback.answer()
        await callback.message.answer("Введите название для нового товара")

    except Exception as e:
        logger.error("Ошибка выдачи категорий для добавления товара %s", e)
        await callback.answer("❌ Возникла не предвиденная ошибка. Попробуйте позже.")
        return

@router.message(AddNewProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    name = message.text.strip()

    await state.update_data(name=name)
    await state.set_state(AddNewProduct.description)

    await message.answer("Введите описание товара")

@router.message(AddNewProduct.description)
async def add_product_name(message: Message, state: FSMContext):
    description = message.text.strip()

    await state.update_data(description=description)
    await state.set_state(AddNewProduct.price)

    await message.answer("Введите цену товара: (целое число)")

@router.message(AddNewProduct.price)
async def add_product_name(message: Message, state: FSMContext):
    price = int(message.text.strip())

    await state.update_data(price=price)
    await state.set_state(AddNewProduct.quantity)

    await message.answer("Введите количество товара")


@router.message(AddNewProduct.quantity)
async def add_product_name(message: Message, state: FSMContext):
    quantity = int(message.text.strip())

    await state.update_data(quantity=quantity)
    await state.set_state(AddNewProduct.photo_path)

    await message.answer("Отправьте фото нового товара")

@router.message(AddNewProduct.photo_path, F.photo)
async def add_product_name(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    try:
        photo = message.photo[-1]

        filename = f"{uuid.uuid4()}.jpg"
        destination = IMAGES_DIR / filename

        await bot.download(
            file=photo,
            destination=destination,
        )

        await state.update_data(
            photo_path=str(destination),
            telegram_file_id=photo.file_id,
        )

        data = await state.get_data()

        caption = (
            f"{data['name']}\n\n"
            f"{data['description']}\n\n"
            f"💰 Стоимость: {data['price']} RUB за 1 шт.\n"
            f"В наличии: {data['quantity']} шт."
        )

        await message.answer_photo(
            photo=FSInputFile(data["photo_path"]),
            caption=caption,
            reply_markup=get_access_add_product(),
        )

    except Exception as e:
        logger.error("Ошибка пред показа товара %s", e)

        await message.answer(
            text="❌ Ошибка добавления товара. Попробуйте позже.",
            reply_markup=get_back_admin_keyboard()
        )

@router.callback_query(F.data.startswith("admin_panel:products:add_confirmation:"))
async def product_add_confirmation(callback: CallbackQuery, state: FSMContext):
    try:
        action = callback.data.split(":")[-1]
        if action == "cancel":
            await state.clear()
            await callback.message.answer(
                text="✖️ Отмена добавления товара",
                reply_markup=get_back_admin_keyboard()
            )

        elif action == "confirm":

            data = await state.get_data()
            await state.clear()

            product_id = await admin_service.add_new_product(data)

            await callback.message.answer(f"✅ Успешное добавление товара {data['name']}, id: {product_id}")

    except Exception as e:
        logger.error("Ошибка отработки хэндлера для добавления товара %s", e)

        await callback.message.answer(
            text="❌ Ошибка добавления товара",
            reply_markup=get_back_admin_keyboard()
        )