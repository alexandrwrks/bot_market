from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.exception.order_ex import (
    NotUserOrder, CostEnoughError,
)
from app.exception.user_ex import NotFoundUserError
from app.keyboards.orders import get_user_orders, get_basket_and_catalog, get_confirm_order

from app.service.order_service import order_service

from app.fsm.order_fsm import OrderFSM

router = Router()


# @router.callback_query(F.data == "confirm_order_btn")
# async def confirm_order(callback: CallbackQuery):
#     await callback.answer()
#
#     await callback.message.edit_text(
#         text="Раздел заказов находится в разработке. Попробуйте позже",
#         reply_markup=get_basket_and_catalog(),
#     )


@router.callback_query(F.data == "orders_btn")
async def orders_btn(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text="Раздел заказов находится в разработке. Попробуйте позже",
        reply_markup=get_basket_and_catalog(),
    )


@router.message(Command("order"))
async def get_order_message(message: Message):

    await message.answer(
        text="Раздел заказов находится в разработке. Попробуйте позже",
        reply_markup=get_basket_and_catalog(),
    )

"""
Настройка FSM для создания заказа пользователю
1) ловим роутером "оформление заказа"
2) начинаем FSM, получаем TG ID
3) продолжение FSM, получение данных для оформления 
"""

@router.callback_query(F.data == "confirm_order_btn")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    try:
        await order_service.check_user_basket_for_order(callback.from_user.id)

        await state.update_data(
            telegram_id=callback.message.from_user.id,
            username=callback.message.from_user.username,
        )

        await state.set_state(OrderFSM.name)

        await callback.message.answer("Введите имя:")

    except CostEnoughError:
        await callback.answer(
            text="В вашей корзине находится товаров стоимостью меньше 5000 рублей.",
            show_alert=True,
        )

    except (NotFoundUserError, Exception):
        await callback.answer(
            text="Ошибка сервера. Попробуйте позже",
            show_alert=True,
        )

@router.message(OrderFSM.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(OrderFSM.surname)

    await message.answer("Введите фамилию:")

@router.message(OrderFSM.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await state.set_state(OrderFSM.phone)

    await message.answer("Введите номер телефона: (+7 123 456 78 90")

@router.message(OrderFSM.phone)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await state.set_state(OrderFSM.email)

    await message.answer("Введите электронную почту:")

@router.message(OrderFSM.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    await state.set_state(OrderFSM.city)

    await message.answer("Введите ваш город:")

@router.message(OrderFSM.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await state.set_state(OrderFSM.address)

    await message.answer("Введите адрес:")

@router.message(OrderFSM.address)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await state.clear()

    try:
        text = (
            "Ваши данные:\n\n"
            f"Имя: {data['name']}\n"
            f"Фамилия: {data['surname']}\n"
            f"Номер телефона: {data['phone']}\n"
            f"Почта: {data['email']}\n"
            f"Город: {data['city']}\n"
            f"Адрес: {data['address']}"
        )

        await message.answer(
            text=text,
            reply_markup=get_confirm_order()
        )

    except Exception:
        await message.answer(
            text="Ошибка. Повторите попытку"
        )