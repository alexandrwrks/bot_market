import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import routers
from app.models.orm.init_db import init_db
from app.models.orm.seed_data import seed_test_data

load_dotenv()


async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения")

    bot = Bot(token)
    dp = Dispatcher()

    await init_db()
    await seed_test_data()

    for router in routers:
        dp.include_router(router)

    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
