import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.orm.config_db import SessionLocal
from app.models.orm.models import Category

logger = logging.getLogger(__name__)

class CategoryRepo:
    async def create_category(self, category_info: dict) -> Optional[Category]:
        async with SessionLocal() as session:
            try:
                category = Category(
                    name=category_info["name"],
                    slug=category_info["slug"],
                    description=category_info.get("description"),
                    
                )

                session.add(category)

                await session.commit()
                await session.refresh(category)

                return category
            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Uniqueness error while creating category: {e}")
                return None
            
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error while creating category: {e}")
                return None
            
    async def get_category_by_slug(self, slug: str) -> Optional[Category]:
        async with SessionLocal() as session:
            try:
                stmt = select(Category).where(Category.slug == slug)
                result = await session.execute(stmt)

                category = result.scalar_one_or_none()
                return category
            
            except SQLAlchemyError as e:
                logger.error(f"Database error while reading category by slug: {e}")
                return None
            
categories_repo = CategoryRepo()