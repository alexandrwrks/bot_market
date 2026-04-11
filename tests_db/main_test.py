import asyncio

from app.models.orm.init_db import init_db
from app.db_repo.categories import CategoryRepo

async def main():
    await init_db()

    repo = CategoryRepo()

    created = await repo.create_category(
        {
            "name": "Protein",
            "slug": "protein",
            "description": "Sports nutrition products",
        }
    )

    print("Created", created.slug if created else None)

    category = await repo.get_category_by_slug("protein")
    print("Found: ", category.name if category else None)

if __name__ == "__main__":
    asyncio.run(main())