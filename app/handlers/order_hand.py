from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.exception.order_ex import (
    NotUserOrder,
)
from app.keyboards.orders import get_user_orders, get_basket_and_catalog

from app.service.order_service import order_service

from app.fsm.order_fsm import OrderFSM

router = Router()


@router.callback_query(F.data == "confirm_order_btn")
async def confirm_order(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text="Раздел заказов находится в разработке. Попробуйте позже",
        reply_markup=get_basket_and_catalog(),
    )


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
