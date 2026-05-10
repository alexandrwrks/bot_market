from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from app.keyboards.basket import get_user_basket

from app.service.basket_service import basket_service

from app.exception.basket_ex import ClearBasketError, NotProductsInBasket
from app.exception.product_ex import NotFoundProductError
from app.exception.user_ex import NotFoundUserError

router = Router()


async def _render_basket(callback: CallbackQuery) -> None:
    telegram_id = callback.from_user.id

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
            await callback.message.answer(
                text=text,
                reply_markup=keyboard,
            )

    except NotFoundProductError:
        await callback.answer(text="Ошибка рендера корзины. Попробуйте позже")


@router.callback_query(F.data == "basket_btn")
async def get_basket(callback: CallbackQuery):
    await callback.answer()
    await _render_basket(callback)


@router.callback_query(F.data == "basket_composition_btn")
async def basket_composition(callback: CallbackQuery):
    await callback.answer()
    await _render_basket(callback)


@router.callback_query(F.data == "clear_btn")
async def clear_basket(callback: CallbackQuery):
    await callback.answer()

    telegram_id = callback.from_user.id

    try:
        await basket_service.clear_basket(telegram_id)

        await callback.answer("Корзина успешна очищена")

        await _render_basket(callback)

    except NotFoundUserError:
        await callback.answer(text="Не найден пользователь", show_alert=True)

    except NotProductsInBasket:
        await callback.answer(text="Товаров нет в корзине", show_alert=True)

    except ClearBasketError:
        await callback.answer(text="Ошибка очистки корзины", show_alert=True)
