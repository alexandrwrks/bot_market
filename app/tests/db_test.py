import aiosqlite
import os
from dotenv import load_dotenv
from dataclasses import dataclass
import asyncio

load_dotenv()

DATA_BASE_NAME = os.getenv("TEST_DATA_BASE_NAME")

@dataclass
class Product:
    category_id: int
    name: str
    description: str
    price: int
    photo_path: str
    quantity: int

@dataclass
class Category:
    name: str
    slug: str

# class TestExecuteTable:
#     def __init__(self):
#         self.db_name = DATA_BASE_NAME

#     async def execute_request(self, query: str, params: tuple, fetch_one = False, fetch_all = False):
#         try:

#             async with aiosqlite.connect(self.db_name) as db:
#                 cursor = await db.execute(query, params)

#                 if fetch_one:
#                     await cursor.fetchone()

#                 if fetch_all:
#                     await cursor.fetchall()

#             await db.commit()

#         except aiosqlite.Error as e:
#             print(f"Ошибка {e}")


class TestCategpryTable:
    def __init__(self):
        self.db_name = DATA_BASE_NAME

    async def init_categories_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS TestCategories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    slug TEXT UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def create_category(self, categories_info: Category):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO TestCategories (name, slug) VALUES (?, ?)", 
                             (categories_info.name, categories_info.slug))

            await db.commit()


class TestProductTable:
    def __init__(self):
        self.db_name = DATA_BASE_NAME

    async def init_products_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS TestProduct (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    photo_path TEXT,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES TestCategories(id)
                )
            """)

            await db.commit()

    async def create_product(self, product_info: Product):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO TestProduct (category_id, name, description, price, photo_path, quantity) VALUES (?, ?, ?, ?, ?, ?)", 
                             (product_info.category_id, product_info.name, product_info.description,
                              product_info.price, product_info.photo_path, product_info.quantity))

            print(f"Успешное добавление товара!")
            await db.commit()
    
    async def get_product_by_category_id(self, category_id: int):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("""
                                SELECT name, description, price, photo_path, quantity
                                FROM TestProduct WHERE category_id = ? AND is_active = TRUE
                                """, (category_id,))
                
                result = await cursor.fetchall()

                return result
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения: {e}")

    async def get_product_names_by_category_id(self, category_id: int):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT id, name FROM TestProduct WHERE category_id = ? AND is_active = TRUE", (category_id,))

                result = await cursor.fetchall()

                return result
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения: {e}")
            return []

    async def get_product_by_id(self, product_id: int):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("""
                        SELECT name, description, price, photo_path
                        FROM TestProduct
                        WHERE id = ? AND is_active = TRUE
                """, (product_id,))

                result = await cursor.fetchall()

                return result
            
        except aiosqlite.Error as e:
            print(f"Ошибка чтения данных: {e}")
            return None

    async def output_info(self, result: list):
        for row in result:
            print(row)


async def main():
    tpt = TestProductTable()

    result = await tpt.get_product_names_by_category_id(1)

    await tpt.output_info(result)

if __name__ == "__main__":
    asyncio.run(main())