import phonenumbers
from phonenumbers import NumberParseException
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.exception.order_ex import (
    CostEnoughError,
)
from app.exception.user_ex import NotFoundUserError
from app.keyboards.orders import (
    get_basket_and_catalog,
    get_confirm_order,
)

from app.service.order_service import order_service

from app.fsm.order_fsm import OrderFSM

router = Router()


class EmailValidator(BaseModel):
    email: EmailStr


class PhoneValidator(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_validator(cls, phone: str) -> str:
        try:
            parsed_phone = phonenumbers.parse(phone)

            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValueError("Неверный номер телефона")

            return phonenumbers.format_number(
                parsed_phone,
                phonenumbers.PhoneNumberFormat.E164,
            )

        except NumberParseException:
            raise ValueError("Неверный номер телефона")


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


@router.callback_query(F.data == "confirm_order_btn")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    try:
        await order_service.check_user_basket_for_order(callback.from_user.id)

        await callback.answer()
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
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())

    await state.set_state(OrderFSM.surname)

    await message.answer("Введите фамилию:")


@router.message(OrderFSM.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())

    await state.set_state(OrderFSM.phone)

    await message.answer("Введите номер телефона:")


@router.message(OrderFSM.phone)
async def process_email(message: Message, state: FSMContext):
    user_input = message.text.strip()

    try:
        validated_data = PhoneValidator(phone=user_input)

        await state.update_data(phone=validated_data.phone)

        await state.set_state(OrderFSM.email)

        await message.answer("Введите электронную почту:")

    except ValueError:
        await message.answer(
            "❌ Неверно введён номер телефона. Проверьте правильность написания.\n\n"
            "Примеры: +77071234567 +79091234567"
        )


@router.message(OrderFSM.email)
async def process_email(message: Message, state: FSMContext):
    user_input = message.text.strip()

    try:
        validated_data = EmailValidator(email=user_input)
        valid_email = validated_data.email

        await state.update_data(email=valid_email)

        await state.set_state(OrderFSM.city)

        await message.answer("Введите ваш город:")

    except ValidationError:
        await message.answer(
            "❌ Не верный формат электронной почты. Проверьте правильность написания почты и повторите ввод"
        )


@router.message(OrderFSM.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await state.set_state(OrderFSM.address)

    await message.answer("Введите адрес:")


@router.message(OrderFSM.address)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    data = await state.get_data()

    text = (
            "Ваши данные:\n\n"
            f"Имя: {data['name']}\n"
            f"Фамилия: {data['surname']}\n"
            f"Номер телефона: {data['phone']}\n"
            f"Почта: {data['email']}\n"
            f"Город: {data['city']}\n"
            f"Адрес: {data['address']}"
        )

    await message.answer(text=text, reply_markup=get_confirm_order())


@router.callback_query(F.data == "done_btn")
async def create_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    try:
        """
        Сохранение заказа в БД и уведомление админов
        """
        await state.clear()

        await callback.message.edit_text(
            text="✅ Заказ успешно оформлен. Мы скоро с вами свяжемся."
        )

    except Exception:
        await callback.message.answer(
            text="❌ Ошибка при создании заказа. Попробуйте ещё раз."
        )

@router.callback_query(F.data == "changes_btn")
async def change_data_for_order(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(text="Изменения данных")
