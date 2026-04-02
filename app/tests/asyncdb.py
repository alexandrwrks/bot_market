import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


load_dotenv()


async def test_async_db():
    database_url = os.getenv("DATA_BASE_URL")

    if not database_url:
        raise ValueError(
            "В .env не найдена переменная DATA_BASE_URL. "
            "Укажи строку подключения к PostgreSQL."
        )

    engine = create_async_engine(
        database_url,
        echo=True,
        pool_pre_ping=True,
    )

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar_one()
            print(f"Подключение к PostgreSQL успешно. Тестовый ответ БД: {value}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_async_db())
