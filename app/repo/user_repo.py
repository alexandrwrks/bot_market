from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, telegram_id: int):
            user = User(
                telegram_id=telegram_id
            )

            self.session.add(user)

    async def get_user(self, telegram_id: int):
        result = await self.session.execute(
            select(User)
            .where(
                User.telegram_id == telegram_id
            ))

        return result.scalar_one_or_none()


    async def update_user_info(
        self
    ):
        ...