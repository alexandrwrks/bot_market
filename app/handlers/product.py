from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from app.keyboards.product import products_keyboard, get_product_keyboard
from app.repo.products import product_repo
from app.repo.basket import basket_repo

router = Router()

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

    telegram_id = callback.from_user.id
    in_cart = await basket_repo.get_product_quantity_in_active_basket(telegram_id, product_id)

    available = product.quantity - in_cart
    if not product or available <= 0:
        await callback.answer("Нет товара в наличие", show_alert=True)
        return 
    

    caption = (
        f"{product.name}\n\n"
        f"Описание: {product.description}\n\n"
        f"Цена: {product.price} руб.\n"
        f"В наличии: {available} шт."
    )

    photo = FSInputFile(product.photo_path)

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=get_product_keyboard(slug, product_id)
    )

    await callback.answer()


# @router.callback_query(F.data.startswith("category:"))
# async def process_taste(callback: CallbackQuery):
#     await callback.answer()
#     category_id = callback.data.split(":")[1]

#     await callback.message.answer(
#         text="Выберите товар:",
#         reply_markup=
#     )