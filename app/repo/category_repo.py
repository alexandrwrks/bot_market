from typing import List, Optional, Tuple

from sqlalchemy import insert, not_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Category, Product
from app.schemas.schema import CategoryCreate


class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, category_info: CategoryCreate) -> Tuple[int, str]:
        result  = await self.session.execute(
            insert(Category)
            .values(
                name=category_info.name,
                slug=category_info.slug,
            )
            .returning(Category.id, Category.name)
        )

        category_id, category_name = result.one()

        return category_id, category_name


    async def get_category_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )

        return result.scalar_one_or_none()

    async def get_existing_categories(self) -> List[Category]:
        """Метод для выдачи названия категорий только тех где есть хоть какой-то товар имея именно эту категорию"""
        result = await self.session.execute(
            select(Category)
            .join(Product, Product.category_id == Category.id)
            .where(
                Category.is_active.is_(True),
                Product.is_active.is_(True),
                Product.quantity > 0,
            )
            .distinct()
            .order_by(Category.id)
        )

        return list(result.scalars().all())

    async def get_categories(self) -> List[Category]:
        result = await self.session.execute(select(Category))
        return list(result.scalars().all())

    async def update_category_active(self, category_id: int) -> None:
        await self.session.execute(
            update(Category)
            .values(is_active=not_(Category.is_active))
            .where(Category.id == category_id)
            .where(Category.id == category_id)
        )