from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from app.keyboards.product import products_keyboard, get_product_keyboard
from app.repo.products import product_repo

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
    
    await callback.message.edit_text(
        text="Выберите товар:",
        reply_markup=products_keyboard(products)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def get_information_about_product(callback: CallbackQuery):
    product_id = callback.data.split(":")[1]

    product = await product_repo.get_product_by_id(product_id)

    if not product:
        await callback.answer("Нет товара в наличие", show_alert=True)
        return 
    
    caption = (
        f"{product.name}\n\n"
        f"Описание: {product.description}\n\n"
        f"Цена: {product.price} руб.\n"
        f"В наличии: {product.quantity} шт."
    )

    photo = FSInputFile(product.photo_path)

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=get_product_keyboard(product_id)
    )

    await callback.answer()


    