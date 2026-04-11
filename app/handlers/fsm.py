from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
class NewProduct(StatesGroup):
    """FSM для добавления нового предмета в БД"""
    category_id: int = State()
    product_name: str = State()
    product_description: str = State()
    product_price: int = State()
    product_quantity: int = State()
    product_photo_path: FSInputFile = State()

@router.message(Command("/add_product"))
@router.callback_query(F.data == "add_new_product")
async def process_add_product(message: Message, state: FSMContext, callback: CallbackQuery):
    await state.set_state(NewProduct.product_name)

    await callback.answer()

    await message.answer("Введите название товара:")

@router.message(NewProduct.product_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(message.text)

    await state.set_state(NewProduct.product_description)

    await message.answer("Введите описание товара:")

@router.message(NewProduct.product_description)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(message.text)

    await state.set_state(NewProduct.product_price)

    await message.answer("Введите описание товара:")

@router.message(NewProduct.product_price)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(message.text)

    await state.set_state(NewProduct.product_quantity)

    await message.answer("Введите количество:")

@router.message(NewProduct.product_quantity)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(message.text)

    await state.set_state(NewProduct.product_photo_path)

    await message.answer("Отправьте фото товара:")

@router.message(NewProduct.product_photo_path)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(message.text)

    await state.clear()

    await message.answer("Товар успешно добавлен в базу")