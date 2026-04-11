import logging
from typing import Optional

from sqlalchemy import select, update, insert, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.orm.config_db import SessionLocal
from app.models.orm.models import Product

from app.handlers.fsm import NewProduct

logger = logging.getLogger(__name__)

class ProductRepo:
    def __init__(self):
        pass

    async def create_product(self,product_info: NewProduct) -> Optional[Product]:
        async with SessionLocal() as session:
            try:
                product = Product(
                    caregory_id=product_info.category_id,
                    name=product_info.product_name,
                    description=product_info.product_description,
                    price=product_info.product_price,
                    quantity=product_info.product_quantity,
                    photo_path=product_info.product_photo_path,
                )

                session.add(product)

                await session.commit()
                await session.refresh(product)

                return product

            except SQLAlchemyError as e:
                logger.error(f"Insert error: {e}")
                return None
        
    async def get_product_names_by_category_id(self, category_id: int):
        async with SessionLocal() as session:
            try:
                stmt = select(Product.id, Product.name).where(
                    Product.category_id == category_id,
                    Product.is_active == True
                )
                
                result = await session.execute(stmt)
                products = result.scalars().all()

                return products
            except SQLAlchemyError as e:
                logger.error(f"Read error: {e}")
                return None
        
    async def get_product_by_id(self, product_id: int):
        async with SessionLocal() as session:
            try:
                stmt = select(Product.name, Product.description, Product.price, Product.photo_path).where(
                    Product.id == product_id,
                    Product.is_active == True,
                )

                result = await session.execute(stmt)

                return result 
            
            except SQLAlchemyError as e:
                logger.error(f"Read error: {e}")
                return None
        
    async def soft_product_delete(self, product_info: NewProduct) -> Optional[Product]:
        async with SessionLocal() as session:
            try:
                stmt = update(Product).where(Product.name == product_info.product_name).values(is_active=0)
                await session.execute(stmt)

                await session.commit()

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Product delete error: {e}")
                return None
        
product_repo = ProductRepo()