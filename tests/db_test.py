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

class TestTables:
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

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

    async def create_category(self, categories_info: Category):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO TestCategories (name, slug) VALUES (?, ?)", 
                             (categories_info.name, categories_info.slug))

            await db.commit()

    async def create_product(self, product_info: Product):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO TestProduct (category_id, name, description, price, photo_path, quantity) VALUES (?, ?, ?, ?, ?, ?)", 
                             (product_info.category_id, product_info.name, product_info.description,
                              product_info.price, product_info.photo_path, product_info.quantity))

            print(f"Успешное добавление товара!")
            await db.commit()


test_categories = Category("Протеин", "protein")


test_products1 = Product(1, "Banana-Strawberry Protein 450 gr", "Протеин со вкусомм банана и клубники", 400, r"images\protein\primekraft_protein_banana_strawberry_450.jpg", 10)
test_products2 = Product(1, "Banana-Strawberry Protein 900 gr", "Протеин со вкусомм банана и клубники", 710, r"images\protein\primekraft_protein_banana_strawberry_900.jpg", 5)
test_products3 = Product(1, "Milk Chocolate Protein 900 gr", "Протеин со вкусомм молочного шоколада", 720, r"images\protein\primekraft_protein_chocolate_900.jpg", 7)
test_products4 = Product(1, "Pina Colado Protein 900 gr", "Протеин со вкусомм пина коладо", 700, r"images\protein\primekraft_protein_pina_colado_900.jpg", 8,)


async def main():
    test = TestTables()

    await test.init_categories_table()
    await test.init_products_table()

    await test.create_category(test_categories)

    await test.create_product(test_products1)
    await test.create_product(test_products2)
    await test.create_product(test_products3)
    await test.create_product(test_products4)

if __name__ == "__main__":
    asyncio.run(main())