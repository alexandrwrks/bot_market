import phonenumbers
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from phonenumbers import NumberParseException
from pydantic import BaseModel, ValidationError, field_validator

from market.bot.keyboards.start import get_start_inline_keyboard
from market.bot.exception.basket_ex import NotProductsInBasket
from market.bot.exception.order_ex import (
    CostEnoughError,
    CreateOrderError,
)
from market.bot.exception.user_ex import NotFoundUserError
from market.bot.fsm.order_fsm import OrderFSM
from market.bot.keyboards.orders import (
    get_confirm_order,
)
from market.bot.service.order_service import order_service

router = Router()


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


@router.callback_query(F.data == "confirm_order_btn")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    try:
        await order_service.check_user_basket_for_order(callback.from_user.id)

        await callback.answer()

        await callback.message.edit_text("Введите ваше имя:")
        await state.set_state(OrderFSM.name)

    except CostEnoughError:
        await callback.answer(
            text="В вашей корзине находится товаров стоимостью меньше 5000 рублей.",
            show_alert=True,
        )

    except NotFoundUserError:
        await callback.answer(
            text="Пользователь не найден. Попробуйте позже",
            show_alert=True,
        )

    except Exception:
        await callback.answer(
            text="Ошибка сервера. Попробуйте позже",
            show_alert=True,
        )


@router.message(OrderFSM.name)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())

    await state.set_state(OrderFSM.phone)

    await message.answer("Введите номер телефона:")


@router.message(OrderFSM.phone)
async def process_email(message: Message, state: FSMContext):
    user_input = message.text.strip()

    try:
        validated_data = PhoneValidator(phone=user_input)

        await state.update_data(phone=validated_data.phone)

        data = await state.get_data()

        text = (
            "Ваши данные:\n\n"
            f"Имя: <b>{data['name']}</b>\n"
            f"Номер телефона: <i>{data['phone']}</i>\n"
        )

        await message.answer(
            text=text, reply_markup=get_confirm_order(), parse_mode="HTML"
        )

    except ValidationError:
        await message.answer(
            "❌ Неверно введён номер телефона. Проверьте правильность написания.\n\n"
            "Примеры: +77071234567 +79091234567"
        )


@router.callback_query(F.data == "done_btn")
async def create_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_data = await state.get_data()

    try:
        await order_service.create_order(
            telegram_id=callback.from_user.id,
            user_data=user_data,
        )
        await state.clear()

        await callback.message.edit_text(
            text="✅ Заказ успешно оформлен. Мы скоро с вами свяжемся.",
            reply_markup=get_start_inline_keyboard(),
        )

    except (CreateOrderError, NotProductsInBasket):
        await callback.message.edit_text(
            text="❌ Ошибка при создании заказа. Попробуйте позже."
        )

    except Exception:
        await callback.message.answer(
            text="❌ Ошибка при создании заказа. Попробуйте ещё раз."
        )


@router.callback_query(F.data == "changes_btn")
async def change_data_for_order(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(text="Изменения данных")
