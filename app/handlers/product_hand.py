from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from app.exception.basket_ex import AddProductToBasketError
from app.exception.product_ex import (
    NotFoundProductError,
    NotEnoughProductQuantityError,
    NoProductsInCategoryError,
)
from app.keyboards.product import products_keyboard, get_product_keyboard

from app.service.basket_service import basket_service
from app.service.product_service import product_service

router = Router()


class AddToCartState(StatesGroup):
    waiting_quantity = State()


@router.callback_query(F.data.startswith("category:"))
async def get_products_by_categories(callback: CallbackQuery):
    """
    Показываем товары выбранной категории
    """
    await callback.answer()

    slug = callback.data.split(":")[1]

    try:
        products = await product_service.get_products_by_category(slug=slug)

        keyboard = products_keyboard(products, slug)

        try:
            await callback.message.edit_text(
                text="Выберите товар:", reply_markup=keyboard
            )
        except TelegramBadRequest:
            await callback.message.answer(text="Выберите товар:", reply_markup=keyboard)

    except NoProductsInCategoryError:
        await callback.message.answer(
            "Нет товаров по выбранной категории. Попробуйте позже"
        )


@router.callback_query(F.data.startswith("product:"))
async def get_information_about_product(callback: CallbackQuery):
    await callback.answer()

    parts = callback.data.split(":")
    slug = parts[1]
    product_id = parts[2]

    try:
        product = await product_service.get_information_about_product(
            product_id=product_id
        )
        if not product:
            raise Exception()
        caption = (
            f"{product.name}\n\n"
            f"Описание: {product.description}\n\n"
            f"Цена: {product.price} руб.\n"
            f"В наличии: {product.quantity} шт."
        )

        await callback.message.answer_photo(
            photo=FSInputFile(product.photo_path),
            caption=caption,
            reply_markup=get_product_keyboard(slug=slug, product_id=product.id),
        )

    except NotFoundProductError:
        await callback.answer(text="Товар не найден", show_alert=True)
        return

    except NotEnoughProductQuantityError:
        await callback.answer(text="Товара нет в наличие", show_alert=True)
        return

    except Exception:
        await callback.answer(
            text="Произошла ошибка. ПОпробуйте позже", show_alert=True
        )


"""
Пользоватлеь нажимает на кнопку "Добавить в корзину"
Сделать так чтобы пользователь писал своё число товаров которое ему нужно
"""


@router.callback_query(F.data.startswith("add_to_cart:"))
async def add_product_to_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    product_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    try:
        product_info = await basket_service.get_product_for_cart_input(
            telegram_id=telegram_id, product_id=product_id
        )

    except NotFoundProductError:
        await callback.message.answer("Этот товар закончился")
        return

    except NotEnoughProductQuantityError:
        await callback.message.answer("Этот товар закончился")
        return

    await state.update_data(product_id=product_id)
    await state.set_state(AddToCartState.waiting_quantity)

    await callback.message.answer(
        f"Введите количество для '{product_info.name}' (1..{product_info.available})",
    )


@router.message(AddToCartState.waiting_quantity)
async def process_product_quantity(message: Message, state: FSMContext):
    data = await state.get_data()

    product_id = int(data["product_id"])
    telegram_id = message.from_user.id

    try:
        quantity = int(message.text)

        await basket_service.add_product_to_basket(
            telegram_id=telegram_id, product_id=product_id, quantity=quantity
        )

    except ValueError:
        await message.answer("Введите число")
        return

    except NotFoundProductError:
        await message.answer("Товар не найден")
        await state.clear()
        return

    except NotEnoughProductQuantityError:
        await message.answer("Недостаточно товара на складе")
        return

    except AddProductToBasketError:
        await message.answer("Не удалось добавить товара в корзину. Попробуйте позже")
        return

    await state.clear()
    await message.answer("Товар добавлен в корзину")
