import logging
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATA_BASE_URL = "postgresql+asyncpg://postgres:postgre123@localhost:5432/test_bot_market"

SQLITE_DATABASE_URL = "sqlite+aiosqlite:///demo.db"

engine = create_async_engine(SQLITE_DATABASE_URL)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("test_bot.log"),
    ],
)

logger = logging.getLogger(__name__)
