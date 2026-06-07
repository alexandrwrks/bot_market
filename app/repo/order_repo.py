from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Order, OrderItem, Product


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(
        self, telegram_id: int, name: str, phone: str, total_price: int
    ):
        result = await self.session.execute(
            insert(Order)
            .values(
                telegram_id=telegram_id,
                name=name,
                phone=phone,
                total_price=total_price,
            )
            .returning(Order.id)
        )
        order_id = result.scalar_one()
        return order_id

    async def add_order_item(
        self,
        order_id: int,
        product_name: str,
        product_id: int,
        quantity: int,
        price: int,
    ):
        await self.session.execute(
            insert(OrderItem).values(
                order_id=order_id,
                product_name=product_name,
                product_id=product_id,
                quantity=quantity,
                price_at_time=price,
            )
        )

    async def get_user_orders(self, telegram_id: int):
        result = await self.session.execute(
            select(Order.id, Order.total_price, Order.status)
            .where(
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

    async def get_count_of_orders(self):
        result = await self.session.execute(select(func.count(Order.id)))
        return result.scalar_one()

    async def get_cost_active_orders(self):
        result = await self.session.execute(
            select(
                func.coalesce(
                    func.sum(OrderItem.quantity * OrderItem.price_at_time),
                    0,
                )
            )
            .join(
                Order,
                Order.id == OrderItem.order_id,
            )
            .where(
                Order.status.in_(
                    [
                        "created",
                        "processing",
                        "paid",
                    ]
                )
            )
        )

        return result.scalar_one()

    async def get_count_of_order(self, telegram_id: int):
        result = await self.session.execute(
            select(func.count(Order.id)).where(Order.telegram_id == telegram_id)
        )
        return result.scalar_one()

    async def get_order_cost(self, telegram_id: int):
        result = await self.session.execute(
            select(func.coalesce(func.sum(Order.total_price), 0)).where(
                Order.telegram_id == telegram_id
            )
        )

        return result.scalar_one()

    async def get_active_users_orders(self):
        result = await self.session.execute(
            select(Order).where(
                Order.status.in_(
                    [
                        "created",
                        "processing",
                        "paid",
                    ]
                )
            )
        )

        return result.scalars().all()

    async def get_user_orders_info(self, telegram_id: int):
        result = await self.session.execute(
            select(Order).where(Order.telegram_id == telegram_id)
        )

        return result.scalars().all()

    async def get_user_order_info(self, order_id: int):
        result = await self.session.execute(select(Order).where(Order.id == order_id))

        return result.scalar_one_or_none()

    async def get_order_items(self, order_id: int):
        result = await self.session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )

        return result.scalars().all()
