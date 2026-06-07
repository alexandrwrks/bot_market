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

                return categories

        except Exception:
            logger.exception("Failed to get categories")
            raise

category_service = CategoryService()
