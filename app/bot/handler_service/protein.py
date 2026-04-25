from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.bot.keyboards.categories import get_catalog_categories, get_protein_options
from app.bot.keyboards.product import get_product_keyboard
from app.repo.basket import basket_repo
from app.repo.categories import categories_repo
from app.repo.products import product_repo

router = Router()


class AddToCartState(StatesGroup):
    waiting_quantity = State()


async def _get_protein_products() -> list[tuple[int, str]]:
    protein_category = await categories_repo.get_category_by_slug("protein")
    if protein_category is None:
        return []
    return await product_repo.get_product_names_by_category_id(protein_category.id)


@router.callback_query(F.data == "protein_btn")
async def show_protein_tastes(callback: CallbackQuery):
    await callback.answer()

    products = await _get_protein_products()
    if not products:
        await callback.message.edit_text(
            text="В категории 'Протеин' пока нет товаров.",
            reply_markup=get_catalog_categories(),
        )
        return

    await callback.message.edit_text(
        text="Выберите вкус:",
        reply_markup=get_protein_options(products),
    )


@router.callback_query(F.data.startswith("protein:"))
async def protein_selected(callback: CallbackQuery):
    await callback.answer()

    try:
        protein_id = int(callback.data.split(":", maxsplit=1)[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный идентификатор товара", show_alert=True)
        return

    product = await product_repo.get_product_by_id(protein_id)
    if product is None:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text = (
        f"{product.name}\n\n"
        f"{product.description}\n"
        f"Цена: {product.price} RUB за штуку\n"
    )

    photo = FSInputFile(product.photo_path)

    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=get_product_keyboard(product.id),
    )


@router.callback_query(F.data == "back_to_protein_list")
async def back_to_protein_list(callback: CallbackQuery):
    await callback.answer()

    products = await _get_protein_products()
    if not products:
        await callback.message.answer(
            text="В категории 'Протеин' пока нет товаров.",
            reply_markup=get_catalog_categories(),
        )
        return

    await callback.message.answer(
        text="Выберите вкус:",
        reply_markup=get_protein_options(products),
    )


@router.callback_query(F.data.startswith("add_to_cart:"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    try:
        product_id = int(callback.data.split(":", maxsplit=1)[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный идентификатор товара", show_alert=True)
        return

    product = await product_repo.get_product_by_id(product_id)
    if product is None:
        await callback.answer("Товар не найден", show_alert=True)
        return

    current_quantity = await basket_repo.get_product_quantity_in_active_basket(
        telegram_id=callback.from_user.id,
        product_id=product.id,
    )
    available_to_add = max(product.quantity - current_quantity, 0)

    await state.set_state(AddToCartState.waiting_quantity)
    await state.update_data(product_id=product.id)

    if available_to_add <= 0:
        await callback.message.answer("Этого товара больше нет в наличии.")
        await state.clear()
        return

    await callback.message.answer(
        f"Введите количество для добавления в корзину.\n"
        f"Доступно: {available_to_add} шт."
    )


@router.message(AddToCartState.waiting_quantity)
async def add_to_cart_quantity(message: Message, state: FSMContext):
    if message.from_user is None:
        await state.clear()
        return

    value = (message.text or "").strip()
    if not value.isdigit():
        await message.answer("Введите целое число, например: 2")
        return

    quantity = int(value)
    if quantity <= 0:
        await message.answer("Количество должно быть больше нуля.")
        return

    data = await state.get_data()
    product_id = data.get("product_id")
    if not isinstance(product_id, int):
        await state.clear()
        await message.answer("Не удалось определить товар. Попробуйте снова.")
        return

    product = await product_repo.get_product_by_id(product_id)
    if product is None:
        await state.clear()
        await message.answer("Товар не найден.")
        return

    current_quantity = await basket_repo.get_product_quantity_in_active_basket(
        telegram_id=message.from_user.id,
        product_id=product.id,
    )
    available_to_add = max(product.quantity - current_quantity, 0)

    if quantity > available_to_add:
        await message.answer(f"Доступно только {available_to_add} шт.")
        return

    item = await basket_repo.add_product_to_basket(
        telegram_id=message.from_user.id,
        product_id=product.id,
        price=product.price,
        quantity=quantity,
    )

    if item is None:
        await message.answer("Не удалось добавить товар в корзину.")
        return

    await state.clear()
    await message.answer(f"Добавлено в корзину: {quantity} шт.")
