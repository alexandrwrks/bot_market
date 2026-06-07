import phonenumbers
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phonenumbers import NumberParseException
from pydantic import BaseModel, ValidationError, field_validator

from app.bot.service.order_service import order_service

router = Router()


class OrderCreateSchema(BaseModel):
    address: str
    full_name: str
    phone: str


class PhoneValidator(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_validator(cls, phone: str) -> str:
        try:
            parsed_phone = phonenumbers.parse(phone)

            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValidationError("Неверный номер телефона")

            return phonenumbers.format_number(
                parsed_phone,
                phonenumbers.PhoneNumberFormat.E164,
            )

        except NumberParseException:
            raise ValidationError("Неверный номер телефона")


def _get_information_text(order: OrderCreateSchema):
    return (
        f"Для оформления заказа нужно указать:"
        f"Адрес: {order.address}\n"
        f"ФИО получателя: {order.full_name}\n"
        f"Телефон: {order.phone}"
    )


def get_order_information(telegram_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="🔄 Изменить адрес", callback_data=f"change_address:{telegram_id}"
    )
    keyboard.button(
        text="🔄 Изменить имя", callback_data=f"change_full_name:{telegram_id}"
    )
    keyboard.button(
        text="🔄 Изменить телефон", callback_data=f"change_phone:{telegram_id}"
    )
    keyboard.button(text="Назад", callback_data="basket_btn")
    keyboard.button(text="Подтвердить", callback_data=f"access_order:{telegram_id}")

    return keyboard.adjust(1).as_markup()


@router.callback_query(F.data == "")
async def callback_query(callback: CallbackQuery):
    try:
        order_info = await order_service.get_info_order(callback.from_user.id)
        order = OrderCreateSchema(**order_info.dict())

        await callback.answer()
        await callback.message.answer(
            text=_get_information_text(order),
            reply_markup=get_order_information(callback.from_user.id),
        )

    except Exception:
        await callback.answer(
            text="Ошибка",
            show_alert=True,
        )
        return
