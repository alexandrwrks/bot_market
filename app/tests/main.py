import asyncio
from app.models.config_db import engine

async def test_async_db():
    async with engine.begin() as conn:
        print("Успешное подключение к базе данных!")

if __name__ == "__main__":
    asyncio.run(test_async_db())