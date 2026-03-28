import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.services.config_hand import routers


load_dotenv()

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)
        
    print("Бот успешно запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
