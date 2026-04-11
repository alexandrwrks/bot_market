from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATA_BASE_URL = "postgresql+asyncpg://postgres:postgre123@localhost:5432/test_bot_market"

SQLITE_DATABASE_URL = "sqlite+aiosqlite:///demo.db"

engine = create_async_engine(
    SQLITE_DATABASE_URL,
    echo=True,
)

SessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass
