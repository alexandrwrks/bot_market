import logging
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config import SessionLocal
from app.database.models import User

logger = logging.getLogger(__name__)


class UserRepo:
    async def create_user(self, telegram_id: int) -> Optional[User]:
        async with SessionLocal() as session:
            try:
                user = User(
                    telegram_id=telegram_id
                )

                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Uniqueness error while creating user: {e}")
                return None

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error while creating user: {e}")
                return None

    async def get_or_create_user(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(User)
                    .where(
                        User.telegram_id == telegram_id
                    ))
                exists_user = result.scalar_one_or_none()
                if exists_user is    None:
                    await self.create_user(telegram_id)

                return True

            except SQLAlchemyError as e:
                logger.error(f"Read error: {e}")
                return None

user_repo = UserRepo()
