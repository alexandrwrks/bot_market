from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from app.bot.exception.basket_ex import ClearBasketError, NotProductsInBasket
from app.bot.exception.product_ex import NotFoundProductError
from app.bot.exception.user_ex import NotFoundUserError
from app.bot.keyboards.basket import (change_basket_product_info,
                                      get_user_basket,
                                      get_user_basket_products)
from app.bot.service.basket_service import basket_service
from app.utils import logger

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

            text += f"💰 Сумма товаров: {total} RUB\n"
            text +=  "ℹ Минимальная сумма заказа - 5000 RUB."

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

    except (Exception, NotFoundProductError) as e:
        logger.warning("Ошибка показа пользовательской корзины %s", e)

        await callback.answer("Ошибка показа корзины. Попробуйте позже")

@router.callback_query(F.data == "menu:basket")
async def get_basket(callback: CallbackQuery):
    await _render_basket(callback)


@router.callback_query(F.data == "basket:composition")
async def basket_composition(callback: CallbackQuery):
    try:
        products = await basket_service.get_basket_position(callback.from_user.id)

        if not products:
            await callback.answer(
                text="Ваша корзина пуста\nДобавьте товар в корзину", show_alert=True
            )
            return

        await callback.answer()
        text = f"Состав корзины ({len(products)} позиций)\n\nВыберите позицию:"
        await callback.message.edit_text(
            text=text, reply_markup=get_user_basket_products(products)
        )

    except Exception as e:
        logger.error("Ошибка выдачи показа товаров внутри корзины %s", e)

        await callback.answer("Ошибка выдачи товаров из корзины")
        return

@router.callback_query(F.data == "basket:clear")
async def clear_basket(callback: CallbackQuery):
    try:
        await basket_service.clear_basket(callback.from_user.id)

        await callback.answer("Корзина успешна очищена")

        await _render_basket(callback)

    except NotProductsInBasket:
        await callback.answer(text="Корзина уже пуста", show_alert=True)

    except (ClearBasketError, NotFoundUserError, Exception) as e:
        logger.error("Ошибка очистки корзины пользователя %s", e)

        await callback.answer(text="Ошибка очистки корзины", show_alert=True)


"""
MVP for get info about product in basket

router: basket:product:product_id

Получаем количество товаров в корзине и их суммарную стоимость по product_id

✅ Товар добавлен в корзину
Название: {product.name}
Количество: {product.quantity} шт
Стоимость за единицу товара: {product.price_at_time} RUB
Сумма: {product.total_price} RUB
| Удалить товар |
| Добавить другой вкус |
| Вернуться в корзину |
"""
@router.callback_query(F.data.startswith("basket:product:"))
async def product_basket(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split(":")[-1])

        info = await basket_service.get_total_price_for_product_in_basket(
            telegram_id=callback.from_user.id, product_id=product_id
        )

        text = (
            f"✅ Товар добавлен в корзину\n"
            f"Название: {info.name}\n"
            f"Количество: {info.quantity} шт.\n"
            f"Стоимость за одну шт: {info.price} RUB.\n"
            f"💰 Сумма: {info.total} RUB"
        )

        await callback.message.edit_text(
            text=text,
            reply_markup=change_basket_product_info(product_id)
        )

    except Exception as e:
        logger.error("Ошибка показа информации о продукте %s", e)

        await callback.answer(
            text="Ошибка получения данных о продукте",
            show_alert=True,
        )

@router.callback_query(F.data.startswith("product:delete:"))
async def delete_basket(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split(":")[-1])

        await basket_service.remove_product_from_basket(telegram_id=callback.from_user.id, product_id=product_id)

        await callback.answer("Успешное удаление товара")
        await _render_basket(callback)

    except Exception as e:
        logger.error("Failed product delete %s", e)

        await callback.answer(
            text="Ошибка удаления товара",
            show_alert=True
        )
        return