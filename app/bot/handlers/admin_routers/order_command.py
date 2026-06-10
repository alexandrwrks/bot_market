import phonenumbers
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from phonenumbers import NumberParseException
from pydantic import BaseModel, field_validator

from app.bot.exception.order_ex import CostEnoughError
from app.bot.exception.user_ex import NotFoundUserError
from app.bot.fsm.order_fsm import (NewAddress, NewFullName, NewPhone,
                                   OrderCreateSchema)
from app.bot.keyboards.orders import (get_back_to_confirm_order,
                                      get_order_information)
from app.bot.service.order_service import order_service
from app.bot.service.user_service import user_service
from app.utils import logger

router = Router()


"""MVP for create order

router: order:confirm

Выдача данных: изначально ❌

Добавление данных в таблицу Users: full_name, address, phone 
сохраняем данные и не удаляем их

Создание заказа с status == created

Добавление full_name, address, phone в таблицу Orders для того заказа который 
создадим после router: order: done
"""



class PhoneValidator(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_validator(cls, phone: str) -> str:
        try:
            parsed_phone = phonenumbers.parse(phone)

            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValueError("❌ Неверный номер телефона")

            return phonenumbers.format_number(
                parsed_phone,
                phonenumbers.PhoneNumberFormat.E164,
            )

        except NumberParseException:
            raise ValueError("❌ Неверный номер телефона")


async def message_send_order_information(
    message: Message,
    order: OrderCreateSchema,
) -> None:
    await message.edit_text(
        text=_get_information_text(order),
        reply_markup=get_order_information(order),
    )

async def callback_send_order_information(
    callback: CallbackQuery,
    order: OrderCreateSchema
) -> None:
    await callback.message.edit_text(
        text=_get_information_text(order),
        reply_markup=get_order_information(order),
    )


def _get_information_text(user_info: OrderCreateSchema):
    return (
        "Для оформления заказа нужно указать:\n\n"
        f"Адрес: {user_info.address if user_info.address else '❌'}\n"
        f"ФИО получателя: {user_info.full_name if user_info.full_name else '❌'}\n"
        f"Телефон: {user_info.phone if user_info.phone else '❌'}"
    )


@router.callback_query(F.data == "order:confirm")
async def menu_order_confirm(callback: CallbackQuery):
    try:
        await order_service.check_user_basket_for_order(callback.from_user.id)

        order = await user_service.get_user_info_for_order(callback.from_user.id)

        await callback.answer()

        await callback_send_order_information(callback, order)

    except CostEnoughError:
        await callback.answer(
            text="В вашей корзине находится товаров стоимостью меньше 5000 рублей.",
            show_alert=True,
        )

    except (Exception, NotFoundUserError) as e:
        logger.exception("Ошибка оформления заказа %s", e)

        await callback.answer(
            text="❌ Ошибка получения данных",
            show_alert=True,
        )
        return

@router.callback_query(F.data == "order:change_address")
async def order_change_address(callback: CallbackQuery, state: FSMContext):
    try:
        """
        Замена адреса
        """
        await state.set_state(NewAddress.address)

        await callback.message.edit_text(
            text="Напишите новый адрес",
            reply_markup=get_back_to_confirm_order(),
        )

    except Exception:
        await callback.answer(
            text="❌ Ошибка изменения адреса. Попробуйте позже",
            show_alert=True,
        )
        return

@router.message(NewAddress.address)
async def new_address(message: Message, state: FSMContext):
    try:
        address = message.text.strip()

        await state.update_data(address=address)
        await state.clear()

        user_info = await user_service.update_user_address(
            address=address, telegram_id=message.from_user.id
        )

        await message_send_order_information(message, user_info)

    except Exception as e:
        logger.exception("Ошибка изменения адреса %s", e)

        await message.answer(
            text="❌ Ошибка изменения адреса",
            reply_markup=get_back_to_confirm_order()
        )



@router.callback_query(F.data == "order:change_full_name")
async def callback_query(callback: CallbackQuery, state: FSMContext):
    try:
        """
        Замена ФИО
        """
        await state.set_state(NewFullName.full_name)

        await callback.message.edit_text(
            text="Напишите ФИО:\n\nПример: Иванов Иван Иванович",
            reply_markup=get_back_to_confirm_order(),
        )

    except Exception:
        await callback.answer(
            text="Ошибка обновления ФИО",
            show_alert=True,
        )
        return

@router.message(NewFullName.full_name)
async def new_full_name(message: Message, state: FSMContext):
    try:
        full_name = message.text.strip()

        await state.update_data(full_name=full_name)
        await state.clear()

        order = await user_service.update_user_full_name(
            full_name=full_name, telegram_id=message.from_user.id
        )

        await message_send_order_information(message, order)

    except Exception:
        logger.error("Ошибка изменения ФИО %s", e)

        await message.answer(
            text="❌ Ошибка изменения ФИО",
            reply_markup=get_back_to_confirm_order()
        )


@router.callback_query(F.data == "order:change_phone")
async def change_phone(callback: CallbackQuery, state: FSMContext):
    try:
        """
        Замена телефона
        """
        await state.set_state(NewPhone.phone)

        await callback.message.edit_text(
            text="Введите номер телефона (например +79991234567):",
            reply_markup=get_back_to_confirm_order(),
        )

    except Exception:
        await callback.answer(
            text="❌ Ошибка обновления телефона",
            show_alert=True,
        )
        return

@router.message(NewPhone.phone)
async def message_new_phone(message: Message, state: FSMContext):
    try:
        phone = message.text.replace(" ", "")
        validated_phone = PhoneValidator(phone=phone)

        await state.update_data(phone=validated_phone.phone)
        await state.clear()

        user_info = await user_service.update_user_phone(
            phone=validated_phone.phone, telegram_id=message.from_user.id
        )

        await message_send_order_information(message, user_info)

    except ValueError as e:
        logger.warning(e)

        await message.answer("Не правильно введён номер телефона\n\nПример: +7 999 000 9900")
        return

    except Exception as e:
        logger.error("Ошибка изменения номера телефона %s", e)

        await message.answer(
            text="❌ Ошибка изменения телефона",
            reply_markup=get_back_to_confirm_order()
        )

@router.callback_query(F.data == "order:done")
async def order_done(callback: CallbackQuery):
    """
    Оформление заказа
    """
    await callback.message.edit_text(
        text="Создание заказа пока в разработке",
        reply_markup=get_back_to_confirm_order(),
    )

