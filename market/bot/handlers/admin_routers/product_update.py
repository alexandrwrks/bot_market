from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile

from market.bot.exception.product_ex import NotFoundProductError
from market.bot.keyboards.admin_keyboards.product_update import (
    get_admin_products_keyboard,
    get_options_for_changes,
    get_exists_catalog_for_admin,
)
from market.bot.service.category_service import category_service
from market.bot.service.product_service import product_service

router = Router()

"""
Usage MVP

router: admin_update_products
get all categories, every category have slug

router: admin_category:{slug}
get all products by slug

router: admin_product:{slug}:{product_id}
get product info bu product_id
"""


@router.callback_query(F.data == "admin_update_products")
async def admin_update_products_callback(callback: CallbackQuery):
    """
    Выбор продукта как у пользователя,
    только после чего идут кнопки на выбор обновления данных:
    Выдать категории → выдать товар по этой категории →
    → нажать на кнопку изменения чего-то

    Выбор изменений: цена, количество, фото, описание, удаление товара(мягкое),
    """
    try:
        categories = await category_service.get_categories()

        try:
            await callback.message.edit_text(
                text="Выберите категорию:",
                reply_markup=get_exists_catalog_for_admin(categories),
            )

        except TelegramBadRequest:
            await callback.message.answer(
                text="Выберите категорию:",
                reply_markup=get_exists_catalog_for_admin(categories),
            )

    except Exception:
        await callback.answer(
            text="Ошибка выдачи категорий. Попробуйте позже.",
            show_alert=True,
        )


@router.callback_query(F.data.startswith("admin_category:"))
async def process_admin_category(callback: CallbackQuery):
    slug = callback.data.split(":")[1]
    try:
        products = await product_service.get_products_by_category(slug=slug)

        try:
            await callback.message.edit_text(
                text="Выберите товар:",
                reply_markup=get_admin_products_keyboard(products, slug),
            )

        except TelegramBadRequest:
            await callback.message.answer(
                text="Выберите товар:",
                reply_markup=get_admin_products_keyboard(products, slug),
            )

    except Exception:
        print("Ошибка на уровне Exception")
        await callback.answer(
            text=f"Ошибка выдачи товаров по категории",
            show_alert=True,
        )


@router.callback_query(F.data.startswith("admin_product:"))
async def process_admin_product(callback: CallbackQuery):
    parts = callback.data.split(":")

    slug = parts[1]
    product_id = int(parts[2])

    try:
        product = await product_service.get_product_information(product_id=product_id)

        caption = (
            f"{product.name}\n\n"
            f"Описание: {product.description}\n\n"
            f"Цена: {product.price} руб.\n"
            f"В наличии: {product.quantity} шт."
        )

        await callback.message.answer_photo(
            photo=FSInputFile(product.photo_path),
            caption=caption,
            reply_markup=get_options_for_changes(slug=slug, product_id=product_id),
        )

    except NotFoundProductError:
        await callback.answer(
            text="Ошибка выдачи товара. Попробуйте позже.",
            show_alert=True,
        )

    except Exception:
        await callback.answer(
            text="Ошибка получения товара. Попробуйте позже.",
            show_alert=True,
        )
