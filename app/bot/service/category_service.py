from typing import List

from app.bot.exception.category_ex import NotCategoryError
from app.database.config import SessionLocal
from app.database.models import Category
from app.repo.category_repo import CategoryRepo
from app.utils import logger


class CategoryService:
    async def get_categories(self) -> List[Category]:
        try:
            async with SessionLocal() as session:
                category_repo = CategoryRepo(session)

                categories = await category_repo.get_existing_categories()
                if not categories:
                    raise NotCategoryError()

                return categories

        except Exception:
            logger.exception("Failed to get categories")
            raise

    async def get_categories_for_admin(self) -> List[Category]:
        try:
            async with SessionLocal() as session:
                category_repo = CategoryRepo(session)

                categories = await category_repo.get_categories()

                logger.info(f"Successfully get categories for admin: count_of_categories={len(categories)}")
                return categories

        except Exception:
            logger.exception("Failed to get categories")
            raise

    async def update_category(self, category_id: int) -> None:
        try:
            async with SessionLocal() as session:
                category_repo = CategoryRepo(session)
                async with session.begin():

                    await category_repo.update_category_active(category_id)

                    logger.info(f"Successfully updated category {category_id}")

        except Exception:
            logger.exception("Failed to update category")
            raise



category_service = CategoryService()
