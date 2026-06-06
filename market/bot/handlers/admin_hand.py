from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from market.bot.exception.user_ex import NotFoundUserError, UserAdminLicense
from market.bot.keyboards.admin_keyboars import (get_admin_inline_keyboard,
                                                 get_back_admin_keyboard,
                                                 get_different_keyboard)
from market.bot.keyboards.start import get_start_inline_keyboard
from market.bot.service.admin_service import admin_service
from market.bot.service.user_service import user_service

router = Router()

WELCOME_MESSAGE = "Панель администратора\nВыберите действие:"


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


@router.callback_query(F.data == "admin_panel:menu")
async def admin_panel_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=WELCOME_MESSAGE, reply_markup=get_admin_inline_keyboard()
    )


@router.callback_query(F.data == "admin_panel:products:add")
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


@router.callback_query(F.data == "admin_admin:orders:view")
async def admin_orders_callback(callback: CallbackQuery):
    await callback.answer()
    """
    Просмотр всех новых заказов которые появились,
    кроме → отменённых и доставленных/выполненных
    """
    try:
        orders = await admin_service.get_admin_orders()

        await callback.message.delete()
        for order in orders:
            text = (
                f"НОМЕР ЗАКАЗА №{order.number}\n"
                f"Имя пользователя: {order.name}\n"
                f"Номер телефона: {order.phone}\n"
                f"Стоимость заказа: {order.total_price}\n"
                f"Статус заказа: {order.status.value}"
            )

            await callback.message.answer(text=text)

        await callback.message.answer(
            text="Выберите следующие действие:",
            reply_markup=get_back_admin_keyboard(),
        )

    except Exception:
        await callback.message.answer(
            text="Ошибка сервера. Попробуйте позже.",
            reply_markup=get_back_admin_keyboard(),
        )


@router.callback_query(F.data == "admin_admin:statistics:view")
async def admin_statistics_callback(callback: CallbackQuery):
    await callback.answer()
    """
    Показ статистики бота:
    1) количество заказов
    2) количество новых пользователей
    """
    try:
        admin_info = await admin_service.get_admin_info()
        keyboard = get_different_keyboard()

        text = (
            f"\tСтатистика:\n"
            f"Пользователи: {admin_info.users}\n"
            f"Заказы: {admin_info.orders}"
        )

        try:
            await callback.message.edit_text(text=text, reply_markup=keyboard)

        except TelegramBadRequest:
            await callback.message.delete()

            await callback.message.answer(text=text, reply_markup=keyboard)

    except Exception:
        await callback.answer(
            text="Ошибка сервера",
            show_alert=True,
        )
