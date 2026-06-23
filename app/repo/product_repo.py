from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.exception.product_ex import NotEnoughProductQuantityError
from app.database.models import Category, Product


class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: str
    price: int
    quantity: int
    photo_path: str


class ProductRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product_info: ProductCreate) -> int:
        product_id = await self.session.execute(
            insert(Product)
            .values(
                category_id=product_info.category_id,
                name=product_info.name,
                description=product_info.description,
                price=product_info.price,
                quantity=product_info.quantity,
                photo_path=product_info.photo_path,
            )
            .returning(Product.id)
        )

        return product_id.scalar_one()

    async def get_product_names_by_category_id(self, category_id: int):
        result = await self.session.execute(
            select(Product.id, Product.name).where(
                Product.category_id == category_id,
                Product.is_active.is_(True),
            )
        )

        products = result.all()

        return products

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.session.execute(
            select(Product).where(
                Product.id == product_id,
                Product.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def soft_product_delete(self, product_id: int):
        product_name = await self.session.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(is_active=False)
            .returning(Product.name)
        )

        return product_name.scalar_one_or_none()

    async def add_quantity(self, product_id: int, quantity: int) -> None:
        await self.session.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(quantity=Product.quantity + quantity)
        )

    async def remove_quantity(self, product_id: int, quantity: int) -> None:
        result = await self.session.execute(
            update(Product)
            .where(Product.id == product_id, Product.quantity >= quantity)
            .values(quantity=Product.quantity - quantity)
        )

        if result.rowcount is None or result.rowcount == 0:
            raise NotEnoughProductQuantityError()

    async def get_all_products(self):
        result = await self.session.execute(select(Product))

        return result.scalars().all()

    async def get_product_by_product_id(self, product_id: int) -> Product:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )

        return result.scalar_one()

    async def get_products_by_slug(
        self, slug: str, include_inactive: bool = False
    ) -> List[Product]:
        # Использование:
        # await repo.get_products_by_slug("category-name")  # для пользователей
        # await repo.get_products_by_slug("category-name", include_inactive=True)  # для админа
        query = (
            select(Product)
            .join(Category, Product.category_id == Category.id)
            .where(Category.slug == slug)
            .order_by(Product.id)
        )

        if not include_inactive:
            query = query.where(
                Category.is_active.is_(True),
                Product.is_active.is_(True),
                Product.quantity > 0,
            )

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_product_price(self, product_id: int, new_price: int) -> None:
        await self.session.execute(
            update(Product).values(price=new_price).where(Product.id == product_id)
        )

    async def get_count_of_all_products(self):
        result = await self.session.execute(select(func.sum(Product.quantity)))

        return result.scalar()

    async def update_product_quantity(self, product_id: int, new_quantity: int) -> None:
        await self.session.execute(
            update(Product)
            .values(quantity=new_quantity)
            .where(Product.id == product_id)
        )
