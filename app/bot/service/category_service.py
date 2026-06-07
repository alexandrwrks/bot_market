from typing import List

from app.bot.exception.category_ex import NotCategoryError
from app.database.config import SessionLocal
from app.database.models import Category
from app.repo.category_repo import CategoryRepo


class CategoryService:
    async def get_categories(self) -> List[Category]:
        async with SessionLocal() as session:
            category_repo = CategoryRepo(session)

            categories = await category_repo.get_existing_categories()
            if not categories:
                raise NotCategoryError()

            return categories


category_service = CategoryService()
