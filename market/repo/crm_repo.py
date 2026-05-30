from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from market.crm.schemas.login import LoginUser

from market.database.models import User
from market.database.config import SessionLocal


class CRMRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    # async def exist_email(self, user: LoginUser):
    #     result = await self._session.execute(
    #         select(User).where(User.email == user.email)
    #     )
    #
    #     return result.scalar_one_or_none()

    async def get_count_of_clients(self) -> int:
        result = await self._session.execute(select(func.count(User.id)))
        count = result.scalar_one()
        return count


class TestUserRepo:
    async def create_user(self, user: LoginUser):
        async with SessionLocal() as session:
            await session.execute(
                insert(User).values(
                    email=user.email,
                    password=user.password,
                )
            )
            await session.commit()
