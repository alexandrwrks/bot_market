import aiosqlite

from config_db import logger, DATA_BASE_NAME


class CategoriesManager:
    def __init__(self):
        self.db_name = DATA_BASE_NAME
    
    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS Categories (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT NOT NULL,
                                 slug TEXT UNIQUE NOT NULL,
                                 description TEXT,
                                 is_active BOOLEAN DEFAULT TRUE
                                 )
                    """)
                
                await db.commit()

        except aiosqlite.Error as e:
            logger.error(f"Error initialization date base: {e}")
            
    async def create_category(self, category_info: dict):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("INSERT INTO Categories (name, slug, description) VALUES (?, ?, ?)", )

                await db.commit()
                
        except aiosqlite.IntegrityError as e:
            await db.rollback()
            logger.error(f"Uniqueness error: {e}")
            
        except aiosqlite.Error as e:
            logger.error(f"Error adding a category: {e}")


    async def get_categories_by_slag(self, slug):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT * FROM Categories WHERE sluf = ?", (slug,))

                result = await cursor.fetchone()
                return result if result else None

        except aiosqlite.Error as e:
            logger.error(f"Data reading error: {e}")
            
categories_manager = CategoriesManager()