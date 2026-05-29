from market.bot.database import models
from market.bot.database.config import lite_engine, Base


async def init_db() -> None:
    async with lite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
