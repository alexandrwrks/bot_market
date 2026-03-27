import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher(bot)

if __name__ == "__main__":
    asyncio.run(main())