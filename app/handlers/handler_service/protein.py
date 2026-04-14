from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from app.db_repo.basket import basket_repo
from app.db_repo.categories import categories_repo
from app.db_repo.products import product_repo
from app.keyboards.categories import get_catalog_categories, get_protein_options
from app.keyboards.product import get_product_keyboard

router = Router()


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
async def add_to_cart(callback: CallbackQuery):
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

    item = await basket_repo.add_product_to_basket(
        telegram_id=callback.from_user.id,
        product_id=product.id,
        price=product.price,
        quantity=1,
    )

    if item is None:
        await callback.answer("Не удалось добавить товар в корзину", show_alert=True)
        return

    await callback.answer("Товар добавлен в корзину")
