import logging
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.orm.config_db import SessionLocal, logger
from app.models.orm.models import User

from aiogram.types import User as TgUser

logger = logging.getLogger(__name__)

class UserRepo:
    async def create_user(self, tg_user: TgUser) -> Optional[User]:
        async with SessionLocal() as session:
            try:
                user = User(
                   telegram_id=tg_user.id,
                   username=tg_user.username,
                   first_name=tg_user.first_name,
                   last_name=tg_user.last_name,
                   is_active=True
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
        
    async def exists_user_by_telegram_id(self, tg_user: TgUser) -> Optional[User]:
        async with SessionLocal() as session:
            try:
                result = await session.execute(select(User).where(User.telegram_id == tg_user.id))
                user = result.scalar_one_or_none()
                
                if user is not None:
                    return user
                
                new_user = await self.create_user(tg_user)

            except SQLAlchemyError as e:
                logger.error(f"Read error: {e}")
                return None
        
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        async with SessionLocal() as session:
            try:
                stmt = select(User).where(User.telegram_id == telegram_id)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

                return user 
            
            except SQLAlchemyError as e:
                logger.error(f"Database error while reading user by telegram_id: {e}")
                return None
        
    async def update_user(self, tg_user: TgUser) -> Optional[User]:
        async with SessionLocal() as session:
            try:
                stmt = (
                    update(User)
                    .where(User.telegram_id == tg_user.id)
                    .values(
                        username=tg_user.username,
                        first_name=tg_user.first_name,
                        last_name=tg_user.last_name,
                    )
                )

                result = await session.execute(stmt)
                
                await session.commit()
                if result.rowcount == 0:
                    return None
                
                return await self.get_user_by_telegram_id(tg_user.id)

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Update user error: {e}")
                return None
        
user_repo = UserRepo()
