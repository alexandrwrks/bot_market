from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards.product import products_keyboard, get_product_keyboard
from app.repo.products import product_repo
from app.repo.basket import basket_repo

router = Router()

class AddToCartState(StatesGroup):
    waiting_quantity = State()

@router.callback_query(F.data.startswith("category:"))
async def get_products_fot_categories(callback: CallbackQuery):
    """
    Показываем товары выбранной категории
    """
    slug = callback.data.split(":")[1]

    products = await product_repo.get_products_by_slug(slug)

    if not products:
        await callback.answer("В этой категории нет товаров:", show_alert=True)
        return 
    
    try:
        await callback.message.edit_text(
            text="Выберите товар:",
            reply_markup=products_keyboard(products, slug)
        )
    except Exception:
        await callback.message.answer(
            text="Выберите товар:",
            reply_markup=products_keyboard(products, slug)
        )

    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def get_information_about_product(callback: CallbackQuery):
    parts = callback.data.split(":")
    slug = parts[1]
    product_id = parts[2]

    product = await product_repo.get_product_by_id(product_id)
    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return
    
    telegram_id = callback.from_user.id
    in_cart = await basket_repo.get_product_quantity_in_active_basket(telegram_id, product_id)
    available = product.quantity - in_cart

    if  available <= 0:
        await callback.answer("Нет товара в наличие", show_alert=True)
        return 
    
    caption = (
        f"{product.name}\n\n"
        f"Описание: {product.description}\n\n"
        f"Цена: {product.price} руб.\n"
        f"В наличии: {available} шт."
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=FSInputFile(product.photo_path),
        caption=caption,
        reply_markup=get_product_keyboard(slug, product_id)
    )

    await callback.answer()



"""
Пользоватлеь нажимает на кнопку "Добавить в корзину"
Сделать так чтобы пользователь писал своё число товаров которое ему нужно
"""
@router.callback_query(F.data.startswith("add_to_cart:"))
async def add_product_to_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    product_id = callback.data.split(":")[1]
    product = await product_repo.get_product_by_id(product_id)
    if not product:
        await callback.message.answer("ТОвар не найден")
        return

    telegram_id = callback.from_user.id
    in_cart = await basket_repo.get_product_quantity_in_active_basket(telegram_id=telegram_id, product_id=product_id)
    available = product.quantity - in_cart

    if available <= 0:
        await callback.message.answer("Этот товар закончился")
        return
    
    await state.update_data(product_id=product_id)
    await state.set_state(AddToCartState.waiting_quantity)

    await callback.message.answer(
        f"Введите количество для '{product.name}' (1..{available}):"
    )

@router.message(AddToCartState.waiting_quantity)
async def add_to_cart_with_quantity(message: Message, state: FSMContext):
    text = (message.text or "").strip()

    if not text.isdigit():
        await message.answer("Введите целое число, например: 1")
        return 
    
    qty = int(text)
    if qty <= 0:
        await message.answer("Количество должно быть больше 0")
        return
    
    data = await state.get_data()
    product_id = data.get("product_id")
    if not product_id:
        await state.clear()
        await message.answer("Сессия истекла. Нажмите 'Добавить в корзину' ещё раз.")
        return
    
    product = await product_repo.get_product_by_id(product_id)
    if not product:
        await state.clear()
        await message.answer("ТОвар не найден")
        return
    
    telegram_id = message.from_user.id
    in_cart = await basket_repo.get_product_quantity_in_active_basket(telegram_id=telegram_id, product_id=product_id)
    available = product.quantity - in_cart

    if available <= 0:
        await state.clear()
        await message.answer(f"Доступно только {available} шт. Введите меньшее число.")
        return
    
    await basket_repo.add_product_to_basket(
        telegram_id=telegram_id,
        product_id=product_id,
        price=product.price,
        quantity=qty
    )

    await product_repo.subtract_product_quantity(
        product_id=product_id,
        quantity=qty
    )

    await state.clear()
    await message.answer(f"Добавлено в корзину: {product.name} x {qty}")