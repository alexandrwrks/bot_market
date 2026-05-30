from market.database.config import SessionLocal
from market.bot.exception.category_ex import NotCategoryError
from market.repo.category_repo import CategoryRepo


class CategoryService:
    async def get_categories(self):
        async with SessionLocal() as session:
            category_repo = CategoryRepo(session)

            categories = await category_repo.get_existing_categories()
            if not categories:
                raise NotCategoryError()

            return categories


category_service = CategoryService()
