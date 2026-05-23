import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import routers
from app.database import init_db
from app.service.user_service import user_service

load_dotenv()

TELEGRAM_ID = [
    1918881124,
]


async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения")

    bot = Bot(token)
    dp = Dispatcher()

    await init_db()
    print("Успешное подключение к базе данных!")

    for router in routers:
        dp.include_router(router)
    print("Успешное подключение роутеров!")

    for telegram_id in TELEGRAM_ID:
        await user_service.get_admin(telegram_id)

    print("Бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"Остановка бота!")
