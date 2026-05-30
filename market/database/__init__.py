from market.database import models
from market.database.config import lite_engine
from market.database.models import Base


async def init_db() -> None:
    async with lite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
