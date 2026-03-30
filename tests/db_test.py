import aiosqlite
import os
from dotenv import load_dotenv

load_dotenv()

DATA_BASE_NAME = os.getenv("DATA_BASE_NAME")

class TestCategories:
    def __init__(self):
        self.db_name = DATA_BASE_NAME

    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS TestCategories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP NOT NULL
                )
            """)

            await db.commit()

    async def create_categories(self, slug: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO TestCategories (slug, created_at) VALUES   (?, CURRENT_TIMESTAMP)", (slug,))

            await db.commit()