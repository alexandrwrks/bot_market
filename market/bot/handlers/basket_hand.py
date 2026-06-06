from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from market.bot.exception.basket_ex import (ClearBasketError,
                                            NotProductsInBasket)
from market.bot.exception.product_ex import NotFoundProductError
from market.bot.exception.user_ex import NotFoundUserError
from market.bot.keyboards.basket import (get_user_basket,
                                         get_user_basket_products)
from market.bot.service.basket_service import basket_service

router = Router()


async def _render_basket(callback: CallbackQuery) -> None:
    telegram_id = callback.from_user.id
    await callback.answer()
    try:
        items, total = await basket_service.render_user_basket(telegram_id)
        keyboard = get_user_basket()

        if not items:
            text = "Ваша корзина пуста.\nМинимальная сумма заказа - 5000 RUB."

        else:
            text = "Ваша корзина\n"
            for name, quantity, price in items:
                text += f"- {name}: {quantity} x {price} RUB\n"

            text += f"Сумма товаров: {total} RUB\n"
            text += "Минимальная сумма заказа - 5000 RUB."

        try:
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
            )

        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=keyboard,
            )

    except NotFoundProductError:
        await callback.answer(text="Ошибка показа корзины. Попробуйте позже")


@router.callback_query(F.data == "menu:basket")
async def get_basket(callback: CallbackQuery):
    await _render_basket(callback)


@router.callback_query(F.data == "basket:composition")
async def basket_composition(callback: CallbackQuery):
    await callback.answer()
    try:
        products = await basket_service.get_basket_position(callback.from_user.id)

        if not products:
            await callback.answer(
                text="Ваша корзина пуста\nДобавьте товар в корзину", show_alert=True
            )
            return

        text = f"Состав корзины ({len(products)} позиций)\n\nВыберите позицию:"
        await callback.message.answer(
            text=text, reply_markup=get_user_basket_products(products)
        )

    except Exception:
        await callback.answer(
            text="Ошибка выдачи товаров из корзины",
        )


@router.callback_query(F.data == "basket:clear")
async def clear_basket(callback: CallbackQuery):
    try:
        await basket_service.clear_basket(callback.from_user.id)

        await callback.answer("Корзина успешна очищена")

        await _render_basket(callback)

    except NotProductsInBasket:
        await callback.answer(text="Корзина уже пуста", show_alert=True)

    except (ClearBasketError, NotFoundUserError):
        await callback.answer(text="Ошибка очистки корзины", show_alert=True)


@router.callback_query(F.data.startswith("basket:product"))
async def product_basket(callback: CallbackQuery):
    try:
        product_id = callback.data.split(":")[-1]
        (
            quantity,
            total_price,
        ) = await basket_service.get_total_price_for_product_in_basket(
            telegram_id=callback.from_user.id, product_id=product_id
        )

        text = (
            f"Товар добавлен в корзину\n"
            f"Количество: {quantity} шт.\n"
            f"Сумма: {total_price} RUB"
        )

        await callback.message.answer(
            text=text,
        )

    except Exception:
        await callback.message.answer(text="Ошибка")
