import asyncio

from app.models.orm.init_db import init_db
from app.models.orm.seed_data import seed_test_data


async def main():
    await init_db()
    await seed_test_data()
    print("Тестовые категории и товары добавлены")


if __name__ == "__main__":
    asyncio.run(main())
