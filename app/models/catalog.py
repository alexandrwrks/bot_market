import aiosqlite
import logging
import os
from dotenv import load_dotenv

load_dotenv()

DATA_BASE_NAME = os.getenv("DATA_BASE_NAME")

class CatalogManager:
    def __init__(self, db_name=DATA_BASE_NAME):
        self.db_name = db_name
    
    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS Catalog (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                description TEXT,
                                price DECINIMAL,
                                amount INTEGER,
                                photo_path TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")

                await db.commit()

        except aiosqlite.Error as e:
            logging.error(f"Ошибка инициализация БД: {e}")