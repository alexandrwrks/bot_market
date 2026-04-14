from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.db_repo.products import product_repo
from app.keyboards.categories import get_categories_for_add_product

router = Router()

CATEGORY_TO_ID = {
    "protein": 1,
    "протеин": 1,
    "geiner": 2,
    "гейнер": 2,
    "creatin": 3,
    "креатин": 3,
    "bcaa": 4,
}


class NewProduct(StatesGroup):
    category_id = State()
    product_name = State()
    product_description = State()
    product_price = State()
    product_quantity = State()
    product_photo_path = State()


@router.message(Command("add_product"))
async def add_product_message(message: Message, state: FSMContext):
    await state.set_state(NewProduct.category_id)
    await message.answer(
        text="Выберите категорию:",
        reply_markup=get_categories_for_add_product(),
    )


@router.callback_query(F.data == "add_new_product")
async def add_product_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewProduct.category_id)
    await callback.answer()
    await callback.message.answer(
        text="Выберите категорию:",
        reply_markup=get_categories_for_add_product(),
    )


@router.callback_query(NewProduct.category_id, F.data.startswith("add_category:"))
async def set_category_from_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    category_slug = callback.data.split(":", maxsplit=1)[1]
    category_id = CATEGORY_TO_ID.get(category_slug)

    if category_id is None:
        await callback.message.answer("Неизвестная категория. Выберите заново.")
        return

    await state.update_data(category_id=category_id)
    await state.set_state(NewProduct.product_name)
    await callback.message.answer("Введите название товара:")


@router.message(NewProduct.category_id)
async def set_category_from_message(message: Message, state: FSMContext):
    category_slug = (message.text or "").strip().lower()
    category_id = CATEGORY_TO_ID.get(category_slug)

    if category_id is None:
        await message.answer("Категория не определена. Используйте: протеин, гейнер, креатин, bcaa.")
        return

    await state.update_data(category_id=category_id)
    await state.set_state(NewProduct.product_name)
    await message.answer("Введите название товара:")


@router.message(NewProduct.product_name)
async def set_product_name(message: Message, state: FSMContext):
    await state.update_data(name=(message.text or "").strip())
    await state.set_state(NewProduct.product_description)
    await message.answer("Введите описание товара:")


@router.message(NewProduct.product_description)
async def set_product_description(message: Message, state: FSMContext):
    await state.update_data(description=(message.text or "").strip())
    await state.set_state(NewProduct.product_price)
    await message.answer("Введите цену товара (целое число):")


@router.message(NewProduct.product_price)
async def set_product_price(message: Message, state: FSMContext):
    price_raw = (message.text or "").strip()
    if not price_raw.isdigit():
        await message.answer("Цена должна быть положительным целым числом. Попробуйте снова.")
        return

    await state.update_data(price=int(price_raw))
    await state.set_state(NewProduct.product_quantity)
    await message.answer("Введите количество товара (целое число):")


@router.message(NewProduct.product_quantity)
async def set_product_quantity(message: Message, state: FSMContext):
    quantity_raw = (message.text or "").strip()
    if not quantity_raw.isdigit():
        await message.answer("Количество должно быть положительным целым числом. Попробуйте снова.")
        return

    await state.update_data(quantity=int(quantity_raw))
    await state.set_state(NewProduct.product_photo_path)
    await message.answer("Отправьте путь к фото (пример: images/protein/item.jpg):")


@router.message(NewProduct.product_photo_path)
async def set_product_photo_path(message: Message, state: FSMContext):
    await state.update_data(photo_path=(message.text or "").strip())

    product_info = await state.get_data()
    created_product = await product_repo.create_product(product_info)

    await state.clear()

    if created_product is None:
        await message.answer("Не удалось сохранить товар. Проверьте логи.")
        return

    await message.answer(f"Товар '{created_product.name}' добавлен.")
