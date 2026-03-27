from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

router = Router()

@router.message(Command("catalog"))
async def cmd_catalog(
    message: Message
) -> None:
    await message.answer(
        "Ниже представлены категории товаров",
        # выдать все категории товаров
    )