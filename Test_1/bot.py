import asyncio
import os
import aiosqlite
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

#база данный#
async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                choice TEXT
            )
        """)
        await db.commit()

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="протеин", callback_data="protein")]
    ])
    await message.answer("Привет, я бот по спорт питу", reply_markup=keyboard)

# Обработка нажатия на кнопку
@dp.callback_query()
async def handle_click(callback: CallbackQuery):
    print(f"Нажата кнопка: {callback.data}")
    
    if callback.data == "protein":
        await callback.answer()
        with open("protein.txt", "r", encoding="utf-8") as f:
            text = f.read()
        print(f"{text}")
        await callback.message.edit_text(text)

# Запуск бота
async def main():
    await init_db()
    print("Bot start!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())