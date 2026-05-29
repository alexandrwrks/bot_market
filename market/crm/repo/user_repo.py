from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from market.crm.schemas.login import LoginUser

from market.crm.database.models import Users
from market.crm.database.config import new_session


class UserRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def exist_email(self, user: LoginUser):
        result = await self._session.execute(
            select(Users).where(Users.email == user.email)
        )

        return result.scalar_one_or_none()

    async def get_count_of_clients(self) -> int:
        result = await self._session.execute(select(func.count(Users.id)))
        count = result.scalar_one()
        return count


class TestUserRepo:
    async def create_user(self, user: LoginUser):
        async with new_session() as session:
            await session.execute(
                insert(Users).values(
                    email=user.email,
                    password=user.password,
                )
            )
            await session.commit()
