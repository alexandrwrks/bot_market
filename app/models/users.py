import aiosqlite
from aiogram.types import User as TgUser
import logging
from dotenv import load_dotenv
import os

load_dotenv()

DATA_BASE_NAME = os.getenv("DATA_BASE_NAME")

class UsersManager:
    def __init__(self):
        self.db_name = DATA_BASE_NAME

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_id INTEGER UNIQUE NOT NULL,
                             username TEXT,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                """)

                await db.commit()

        except aiosqlite.Error as e:
            logging.error(f"Database error: {e}")

    async def add_user_data(self, user_info: dict):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    INSERT INTO Users (user_id, username, created_at = CURRENT_TIMESTAMP) VALUES (?, ?) 
                """, (
                    user_info["user_id"],
                    user_info["name"]
                ))

                await db.commit()

        except aiosqlite.IntegrityError as e:
            logging.error(f"Unique error: {e}")

        except aiosqlite.Error as e:
            logging.error(f"Error: {e}")

    async def check_user_id(self, tg_user_id: int):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT user_id FROM Users WHERE user_id = ?",
                                          (tg_user_id,))
                
                result = await cursor.fetchone()

                return result

        except aiosqlite.Error as e:
            logging.error(f"")

users_manager = UsersManager()