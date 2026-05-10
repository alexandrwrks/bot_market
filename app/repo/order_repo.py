from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BasketItem, Order, OrderItem, Product


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order_from_active_basket(self, basket_id: int):
        new_order = Order(
        )
        return new_order

    async def get_user_orders(self, telegram_id: int):
        result = await self.session.execute(
            select(Order.id, Order.total_price, Order.status).where(
                Order.telegram_id == telegram_id,
            )
            .order_by(Order.created_at.desc())
        )

        return [
            (order_id, total_price, status)
            for order_id, total_price, status in result.all()
        ]

    async def get_order_details(self, telegram_id: int, order_id: int):
        result = await self.session.execute(
            select(
                Order.id,
                Order.total_price,
                Order.status,
                Product.name,
                OrderItem.quantity,
                OrderItem.price_at_time,
            )
            .join(OrderItem, OrderItem.order_id == Order.id)
            .join(Product, Product.id == OrderItem.product_id)
            .where(
                Order.id == order_id,
                Order.telegram_id == telegram_id,
            )
        )

        return [
            (order_id, total_price, status, product_name, quantity, price)
            for order_id, total_price, status, product_name, quantity, price in result.all()
        ]
