import asyncio

from aiogram import Bot, Dispatcher

from app.handlers import routers
from app.database import init_db
from app.service.user_service import user_service

from app.config import settings


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    await init_db()
    print("Успешное подключение к базе данных!")

    for router in routers:
        dp.include_router(router)
    print("Успешное подключение роутеров!")

    for telegram_id in settings.ADMIN_IDS:
        await user_service.get_admin(telegram_id)

    print("Бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"Остановка бота!")
