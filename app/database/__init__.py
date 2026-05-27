from .config import lite_engine, Base
from app.database import models


async def init_db() -> None:
    async with lite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
