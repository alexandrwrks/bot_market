from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.exception.order_ex import NotUserOrder
from app.keyboards.orders import get_user_orders

from app.service.order_service import order_service

router = Router()


@router.message(Command("order"))
async def get_order_message(message: Message):
    try:
        text = "Раздел заказов в доработке."
        keyboard = get_user_orders()

        await message.answer(text=text, reply_markup=keyboard)
    except Exception:
        await message.answer("Ошибка сервера. Попробуйте позже")


@router.callback_query(F.data == "orders_btn")
async def get_orders(callback: CallbackQuery):
    await callback.answer()

    orders = await order_service.get_user_orders(callback.from_user.id)

    if not orders:
        await callback.answer(text="У Вас пока нет заказов.", show_alert=True)
    else:
        await callback.message.edit_text(text="Ваши заказы:")

        for order_id, total_price, status in orders:
            await callback.message.answer(
                text=f"ЗАКАЗ №{order_id}",
                reply_markup=get_user_orders([(order_id, total_price, status)]),
            )


@router.callback_query(F.data.startswith("order:"))
async def get_order_details(callback: CallbackQuery):
    await callback.answer()

    try:
        order_id = int(callback.data.split(":", maxsplit=1)[1])

    except (IndexError, ValueError):
        await callback.answer("Некорректный номер заказа", show_alert=True)
        return

    order_items = await order_service.get_order_details(
        telegram_id=callback.from_user.id, order_id=order_id
    )

    if not order_items:
        await callback.answer(text="Заказ не найден Попробуйте позже", show_alert=True)
        return

    first_item = order_items[0]

    order_id = first_item[0]
    total_price = first_item[1]
    status = first_item[2]

    lines = [
        f"Заказ №{order_id}",
        f"Статус: {status}",
        f"Сумма: {total_price} RUB\n\n",
        "Товары:",
    ]

    for _, _, _, product_name, quantity, price in order_items:
        lines.append(f"- {product_name}: {quantity} x {price} RUB")

    text = "\n".join(lines)

    await callback.message.edit_text(
        text=text,
    )
