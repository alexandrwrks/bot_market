from app.database.config import SessionLocal, logger
from app.exception.category_ex import NotCategoryError
from app.repo.category_repo import CategoryRepo


class CategoryService:
    async def get_categories(self):
        async with SessionLocal() as session:
            category_repo = CategoryRepo(session)

            categories = await category_repo.get_existing_categories()
            if not categories:
                raise NotCategoryError()

            return categories


category_service = CategoryService()
