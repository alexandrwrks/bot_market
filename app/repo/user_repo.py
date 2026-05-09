from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, telegram_id: int) -> Optional[User]:
            user = User(
                telegram_id=telegram_id
            )

            self.session.add(user)
            return user

    async def get_or_create_user(self, telegram_id: int):
        result = await self.session.execute(
            select(User)
            .where(
                User.telegram_id == telegram_id
            ))
        exists_user = result.scalar_one_or_none()
        if exists_user is None:
            await self.create_user(telegram_id)

        return True

    async def update_use_info(
        self
    ):
        ...