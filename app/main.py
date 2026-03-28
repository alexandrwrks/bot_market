import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.services.config_hand import routers
from app.models.catalog import catalog_manager
from app.models.users import users_manager


load_dotenv()

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    await catalog_manager.init_db()
    await users_manager.init_db()

    for router in routers:
        dp.include_router(router)
        
    print("Бот успешно запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
