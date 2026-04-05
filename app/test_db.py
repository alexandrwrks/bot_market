import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

DATABASE_URL = "postgresql+asyncpg://postgres:postgre123@localhost:5432/test_bot_market"


class Base(DeclarativeBase):
    pass


class TestUser(Base):
    __tablename__ = "test_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column()


class TestProduct(Base):
    __tablename__ = "test_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()


async def main():
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        # создаём таблицы
        await conn.run_sync(Base.metadata.create_all)

        # вставляем данные
        await conn.execute(
            TestUser.__table__.insert(),
            [{"name": "Alex", "age": 18}]
        )

        await conn.execute(
            TestProduct.__table__.insert(),
            [{"title": "Protein", "price": 400}]
        )

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())