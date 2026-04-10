from __future__ import annotations

from tests_db.config import engine, Base

from tests_db.category_repo import Category

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)