from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.exception.user_ex import UserAdminLicense, NotFoundUserError
from app.keyboards.start import get_start_inline_keyboard, get_admin_inline_keyboard
from app.service.user_service import user_service

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message):
    try:
        await user_service.admin_panel(message.from_user.id)

        text = (
            "Панель администратора\n"
            "Выберите действие:"
        )

        await message.answer(
            text="Панель администратора", reply_markup=get_admin_inline_keyboard()
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
