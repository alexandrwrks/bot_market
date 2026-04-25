from sqlalchemy import select

from app.database.config import SessionLocal
from app.database.models import Category, Product


CATEGORIES = [
    {
        "name": "Протеин",
        "slug": "protein",
        "description": "Протеиновые смеси",
    },
    {
        "name": "Гейнер",
        "slug": "geiner",
        "description": "Высококалорийные смеси",
    },
    {
        "name": "Креатин",
        "slug": "creatin",
        "description": "Добавки с креатином",
    },
    {
        "name": "БЦАА",
        "slug": "bcaa",
        "description": "Аминокислоты BCAA",
    },
]

TEST_PRODUCTS = [
    {
        "category_slug": "protein",
        "name": "PrimeKraft Whey Банан-Клубника 900 г",
        "description": "Сывороточный протеин со вкусом банана и клубники.",
        "price": 2290,
        "quantity": 20,
        "photo_path": "images/protein/primekraft_protein_banana_strawberry_900.jpg",
    },
    {
        "category_slug": "protein",
        "name": "PrimeKraft Whey Шоколад 900 г",
        "description": "Сывороточный протеин со вкусом шоколада.",
        "price": 2290,
        "quantity": 18,
        "photo_path": "images/protein/primekraft_protein_chocolate_900.jpg",
    },
    {
        "category_slug": "protein",
        "name": "PrimeKraft Whey Пина Колада 900 г",
        "description": "Сывороточный протеин со вкусом пина колада.",
        "price": 2390,
        "quantity": 15,
        "photo_path": "images/protein/primekraft_protein_pina_colado_900.jpg",
    },
]


async def seed_test_data() -> None:
    async with SessionLocal() as session:
        category_ids: dict[str, int] = {}

        for category_data in CATEGORIES:
            result = await session.execute(select(Category).where(Category.slug == category_data["slug"]))
            category = result.scalar_one_or_none()

            if category is None:
                category = Category(**category_data)
                session.add(category)
                await session.flush()

            category_ids[category.slug] = category.id

        for product_data in TEST_PRODUCTS:
            result = await session.execute(select(Product).where(Product.name == product_data["name"]))
            existing = result.scalar_one_or_none()
            if existing is not None:
                continue

            session.add(
                Product(
                    category_id=category_ids[product_data["category_slug"]],
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                    photo_path=product_data["photo_path"],
                )
            )

        await session.commit()
