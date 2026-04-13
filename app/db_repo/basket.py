from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.orm.config_db import SessionLocal, logger
from app.models.orm.models import Basket, BasketItem, Product

class BasketRepo:
    def __init__(self):
        pass

    async def get_or_create_basket(self, telegram_id: int) -> Basket:
        async with SessionLocal() as session:
            try:
                result = await session.execute(select(Basket).where(Basket.telegram_id == telegram_id, Basket.status == "active"))
                
                basket = result.scalar_one_or_none()

                if basket is not None:
                    return basket
                
                basket = Basket(telegram_id=telegram_id, status="active")
                session.add(basket)
                await session.commit()
                await session.refresh(basket)

                return basket
        
            except IntegrityError as e:
                logger.error(f"Unique error: {e}")
                return None
            
            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                return None
            
    async def add_product_to_basket(self, telegram_id: int, product: Product, quantity: int = 1) -> BasketItem:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_basket(telegram_id)

                result = await session.execute(select(BasketItem).where(
                    BasketItem.basket_id == basket.id,
                    BasketItem.id == product.id
                ))

                basket_item = result.scalar_one_or_none()

                if basket_item is not None:
                    basket_item.quantity += quantity
                    await session.commit()
                    await session.refresh(basket_item)
                    return basket_item
                
                basket_item = Basket(
                    basket_id=basket.id,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_time=product.price
                )
                session.add(basket_item)
                await session.commit()
                await session.refresh(basket_item)

                return basket_item
            
            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                return None
            
basket_repo = BasketRepo()