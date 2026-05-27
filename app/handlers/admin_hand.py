from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.exception.user_ex import UserAdminLicense, NotFoundUserError
from app.keyboards.admin_keyboars import (
    get_back_admin_keyboard,
    get_admin_inline_keyboard,
)
from app.keyboards.start import get_start_inline_keyboard
from app.service.user_service import user_service

router = Router()

WELCOME_MESSAGE = "Панель администратора\nВЫберите действие:"


@router.message(Command("admin"))
async def admin_command(message: Message):
    try:
        await user_service.admin_panel(message.from_user.id)

        await message.answer(
            text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
        )

    except UserAdminLicense:
        await message.answer(
            text="У Вас нет прав на использование админки",
            reply_markup=get_start_inline_keyboard(),
        )

    except NotFoundUserError:
        await message.answer(
            text="Команда не временно не работает. Попробуйте позже",
            reply_markup=get_start_inline_keyboard(),
        )

    except Exception:
        await message.answer(
            text="Ошибка со стороны сервера. Попробуйте позже.",
            reply_markup=get_start_inline_keyboard(),
        )


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
    )


@router.callback_query(F.data == "admin_products")
async def admin_products_callback(callback: CallbackQuery):
    """
    Добавить FSM для добавления товара:
    1) выбор категории → добавляем новую если её нет в БД
    2) FSM для написания данных о товаре
    3) подтверждение добавления товара
    """
    await callback.answer()
    await callback.message.edit_text(
        text="Добавление товаров находится в разработке. Попробуйте позже.",
        reply_markup=get_back_admin_keyboard(),
    )


@router.callback_query(F.data == "admin_update_products")
async def admin_update_products_callback(callback: CallbackQuery):
    """
    Выбор продукта как у пользователя,
    только после чего идут кнопки на выбор обновления данных:

    """
    await callback.answer()
    await callback.message.edit_text(
        text="Обновление товаров находится в разработке. Попробуйте позже",
        reply_markup=get_back_admin_keyboard(),
    )


@router.callback_query(F.data == "admin_orders")
async def admin_orders_callback(callback: CallbackQuery):
    """
    Просмотр всех новых заказов которые появились,
    кроме → отменённых и доставленных/выполненных
    """
    await callback.answer()
    await callback.message.edit_text(
        text="Раздел заказов находится в разработке. Попробуйте позже.",
        reply_markup=get_back_admin_keyboard(),
    )


@router.callback_query(F.data == "admin_statistics")
async def admin_statistics_callback(callback: CallbackQuery):
    """
    Показ статистики бота:
    1) количество заказов
    2) количество новых пользователей
    """
    await callback.answer()
    await callback.message.edit_text(
        text="Раздел статистика находится в разработке. Попробуйте позже.",
        reply_markup=get_back_admin_keyboard(),
    )
