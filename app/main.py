import asyncio
import os
# import app.models.config_db

from aiogram import Bot, Dispatcher

from app.services.config_hand import routers
from app.models.sql.products_db import catalog_manager
from app.models.orm.init_db import init_db

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    await init_db()

    for router in routers:
        dp.include_router(router)
        
    print("Бот успешно запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
