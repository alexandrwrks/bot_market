from aiogram.types import User as TgUser
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: TgUser):
        await self.session.execute(
            insert(User).values(
                telegram_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )
        )

    async def get_user(self, telegram_id: int):
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )

        return result.scalar_one_or_none()

    async def get_user_admin(self, telegram_id: int):
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )

        return result.scalars()

    async def update_admin(self, telegram_id: int):
        await self.session.execute(
            update(User).where(User.telegram_id == telegram_id).values(admin=True)
        )

    async def get_all_users(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_count_users(self):
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar_one_or_none()
