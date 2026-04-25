from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.config import SessionLocal, logger
from app.database.models import BasketItem, Order, OrderItem, Product
from app.repo.basket import basket_repo


class OrderRepo:
    async def create_order_from_active_basket(self, telegram_id: int) -> Optional[Order]:
        async with SessionLocal() as session:
            try:
                basket = await basket_repo.get_or_create_active_basket(telegram_id, session=session)
                if basket is None:
                    return None

                result = await session.execute(
                    select(BasketItem, Product)
                    .join(Product, Product.id == BasketItem.product_id)
                    .where(BasketItem.basket_id == basket.id)
                )
                rows = result.all()
                if not rows:
                    return None

                for basket_item, product in rows:
                    if product.quantity < basket_item.quantity:
                        logger.error(f"Not enough quantity for product_id={product.id}")
                        return None

                total_price = sum(item.quantity * item.price_at_time for item, _ in rows)

                order = Order(
                    telegram_id=telegram_id,
                    total_price=total_price,
                    status="created",
                )
                session.add(order)
                await session.flush()

                order_items: list[OrderItem] = []
                for basket_item, product in rows:
                    product.quantity -= basket_item.quantity
                    order_items.append(
                        OrderItem(
                            order_id=order.id,
                            product_id=basket_item.product_id,
                            quantity=basket_item.quantity,
                            price_at_time=basket_item.price_at_time,
                        )
                    )

                session.add_all(order_items)
                basket.status = "ordered"

                await session.commit()
                await session.refresh(order)
                return order

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Order create error: {e}")
                return None

    async def get_user_orders(self, telegram_id: int) -> list[Order]:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(Order)
                    .where(Order.telegram_id == telegram_id)
                    .order_by(Order.created_at.desc())
                )
                return list(result.scalars().all())

            except SQLAlchemyError as e:
                logger.error(f"Order list read error: {e}")
                return []

    async def get_order_by_id(self, telegram_id: int, order_id: int) -> Optional[Order]:
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(Order).where(
                        Order.id == order_id,
                        Order.telegram_id == telegram_id,
                    )
                )
                return result.scalar_one_or_none()

            except SQLAlchemyError as e:
                logger.error(f"Order read error: {e}")
                return None


order_repo = OrderRepo()
