from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from market.database.models import Category, Product


class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, category_info: dict) -> Optional[Category]:
        category = Category(
            name=category_info["name"],
            slug=category_info["slug"],
            description=category_info.get("description"),
        )

        self.session.add(category)

        return category

    async def get_category_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )

        return result.scalar_one_or_none()

    async def get_existing_categories(self) -> list[Category]:
        """Метод для выдачи названия категорий только тех где есть хоть какой-то товар имея именно эту категорию"""
        result = await self.session.execute(
            select(Category)
            .join(Product, Product.category_id == Category.id)
            .where(
                Category.is_active == True,
                Product.is_active == True,
                Product.quantity > 0,
            )
            .distinct()
            .order_by(Category.id)
        )

        return list(result.scalars().all())
