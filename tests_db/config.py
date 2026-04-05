from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATA_BASE_URL = "postgresql+asyncpg://postgres:postgre123@localhost:5432/test_bot_market"
LITE_DATA_BASE_URL = "sqlite+aiosqlite:///test_bot_market.db"

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    LITE_DATA_BASE_URL,
    echo=True,
)

SessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False,
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
