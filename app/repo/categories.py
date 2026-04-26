import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.config import SessionLocal
from app.database.models import Category, Product

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
                result = await session.execute(
                    select(Category)
                    .where(Category.slug == slug)
                )

                return result.scalar_one_or_none()

            except SQLAlchemyError as e:
                logger.error(f"Database error while reading category by slug: {e}")
                return None
            

    async def get_existing_categories(self) -> list[Category]:
        """Метод для выдачи названия категорий только тех где есть хоть какой-то товар имея именно эту категорию"""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Category)
                .join(Product, Product.category_id == Category.id)
                .where(
                    Category.is_active == True,
                    Product.is_active == True,
                    Product.quantity > 0
                )
                .distinct()
                .order_by(Category.id)
            )

            return list(result.scalars().all())


categories_repo = CategoryRepo()
