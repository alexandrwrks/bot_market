import logging

from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from app.database.config import SessionLocal, logger
from app.database.models import Product

from dataclasses import dataclass

@dataclass
class NewProduct:
    category_id: int
    name: str
    description: str
    price: int
    quantity: int
    photo_path: str


class ProductRepo:
    async def create_product(self, product_info: NewProduct) -> Optional[Product]:
        async with SessionLocal() as session:
            try:
                product = Product(
                    category_id=product_info.category_id,
                    name=product_info.name,
                    description=product_info.description,
                    price=product_info.price,
                    quantity=product_info.quantity,
                    photo_path=product_info.photo_path,
                )

                session.add(product)
                await session.commit()
                await session.refresh(product)
                return product

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Insert error: {e}")
                return None

    async def get_product_names_by_category_id(self, category_id: int) -> list[tuple[int, str]]:
        async with SessionLocal() as session:
            try:
                stmt = select(Product.id, Product.name).where(
                    Product.category_id == category_id,
                    Product.is_active.is_(True),
                )
                result = await session.execute(stmt)
                return result.all()

            except SQLAlchemyError as e:
                logger.error(f"Read error: {e}")
                return []

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        async with SessionLocal() as session:
            try:
                stmt = select(Product).where(
                    Product.id == product_id,
                    Product.is_active.is_(True),
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()

            except SQLAlchemyError as e:
                logger.error(f"Read error: {e}")
                return None

    async def soft_product_delete(self, product_id: int) -> bool:
        async with SessionLocal() as session:
            try:
                stmt = update(Product).where(Product.id == product_id).values(is_active=False)
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount > 0

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Product delete error: {e}")
                return False


product_repo = ProductRepo()
