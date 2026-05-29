from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from market.bot.keyboards.orders import get_basket_and_catalog

router = Router()


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
