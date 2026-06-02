from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from market.bot.exception.order_ex import NotUserOrder
from market.bot.keyboards.orders import get_basket_and_catalog, get_detail_keyboard
from market.bot.service.order_service import order_service

router = Router()


@router.callback_query(F.data == "orders_btn")
async def orders_btn(callback: CallbackQuery):
    try:
        orders = await order_service.get_user_orders(callback.from_user.id)

        await callback.answer()

        for order in orders:
            text = (
                f"Номер заказа: {order.id}\n"
                f"Стоимость заказа: {order.total_price}\n"
                f"Статус: {order.status}\n"
                f"Создание заказа: {order.created_at}"
            )

            await callback.message.answer(
                text=text,
                reply_markup=get_detail_keyboard(order.id), # Кнопка подробнее что вывести что находится в заказе
            )

        await callback.message.answer(
            text="Выберите действие:",
            reply_markup=get_basket_and_catalog(),
        )

    except (Exception, NotUserOrder):
        await callback.answer(
            text="У вас нет активных заказов",
            show_alert=True,
        )


@router.message(Command("order"))
async def get_order_message(message: Message):
    try:
        orders = await order_service.get_user_orders(message.from_user.id)

        for order in orders:
            text = (
                f"Номер заказа: {order.id}\n"
                f"Стоимость заказа: {order.total_price}\n"
                f"Статус: {order.status}\n"
                f"Создание заказа: {order.created_at}"
            )

            await message.answer(
                text=text,
                reply_markup=get_detail_keyboard(order.id), # Кнопка подробнее что вывести что находится в заказе
            )

        await message.answer(
            text="Выберите действие:",
            reply_markup=get_basket_and_catalog(),
        )

    except (Exception, NotUserOrder):
        await message.answer(
            text="У вас нет активных заказов",
            reply_markup=get_basket_and_catalog(),
        )

@router.callback_query(F.data.startswith("detail_order:"))
async def process_detail_order(callback: CallbackQuery):
    await callback.answer()
    order_id = int(callback.data.split(":")[1])
    try:
        order = await order_service.get_user_order_info(order_id=order_id)

        items_text = ""
        for item in order.items:
            items_text += (
                f"• {item.name}\n"
                f"  {item.quantity} шт x {item.price} = {item.total} ₽\n\n"
            )

        text = (
            f"Номер заказа: {order.id}\n"
            f"Стоимость заказа: {order.total_price}\n"
            f"Статус: {order.status}\n"
            f"Создание заказа: {order.created_at}\n"
            f"{items_text}"
        )

        await callback.message.answer(
            text=text,
            reply_markup=get_basket_and_catalog(),
        )

    except NotUserOrder:
        await callback.answer(
            text="Ошибка нет такого заказа. Попробуйте позже",
            show_alert=True,
        )
    except Exception:
        await callback.answer(
            text="Ошибка показа заказа. Попробуйте позже",
            show_alert=True,
        )