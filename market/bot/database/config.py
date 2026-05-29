import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from market.bot.config import settings

# engine = create_async_engine(settings.DATABASE_URL)
lite_engine = create_async_engine(settings.SQLITE_DATABASE_URL)

SessionLocal = async_sessionmaker(
    lite_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(
            filename="bot_market.log",
            encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger(__name__)
