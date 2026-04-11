import os
from dotenv import load_dotenv
from vkbottle import Bot
from .keyboards import bl


load_dotenv()

TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=TOKEN, labeler=bl)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.run_forever()