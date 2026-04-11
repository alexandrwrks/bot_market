import aiosqlite

from app.models.sql.config_db import logger, DATA_BASE_NAME


class ProductManager:
    def __init__(self):
        self.db_name = DATA_BASE_NAME
    
    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_id INT NOT NULL,
                        name TEXT NOT NULL,
                        description TEXT,
                        price INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        photo_path TEXT,
                        is_active BOOLEAN DEFAULT TRUE
                        )
                """)


                await db.commit()

        except aiosqlite.Error as e:
            logger.error(f"Ошибка инициализация БД: {e}")

    async def get_option_products(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT name, description, price, quantity, photo_path FROM Products WHERE is_active = TRUE AND categoty_id")

                result = await cursor.fetchall()

                return result if result else None
            
        except aiosqlite.Error as e:
            logger.error(f"Ошибка чтения данных: {e}")


    async def create_product(self, ):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("INSERT INTO Products (category_id, name, description, price, quantity, photo_path) VALUES (?, ?, ?, ?, ?, ?)")

                await db.commit()

        except aiosqlite.Error as e:
            logger.error(f"Ошибка добавления: {e}")

catalog_manager = ProductManager()