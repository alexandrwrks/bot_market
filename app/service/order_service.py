from app.database.config import SessionLocal, logger
from app.exception.order_ex import NotUserOrder

from app.repo.order_repo import OrderRepo
from app.repo.product_repo import ProductRepo
from app.repo.basket_repo import BasketRepo


class OrderService:
    async def create_order(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
                async with session.begin():
                    product_repo = ProductRepo(session)
                    basker_repo = BasketRepo(session)
                    order_repo = OrderRepo(session)

            except Exception as e:
                logger.error(e)
                raise

    async def get_user_orders(self, telegram_id: int):
        """Выдаём все заказы которые есть у пользователя"""
        async with SessionLocal() as session:
            try:
                order_repo = OrderRepo(session)

                orders = await order_repo.get_user_orders(telegram_id)

                if not orders:
                    raise NotUserOrder()

                return orders

            except NotUserOrder:
                return []

            except Exception:
                logger.exception("Ошибка выдачи заказов пользователя=%s", telegram_id)
                return []

    async def get_order_details(self, telegram_id: int, order_id: int):
        async with SessionLocal() as session:
            order_repo = OrderRepo(session)
            try:
                order_items = await order_repo.get_order_details(
                    telegram_id=telegram_id, order_id=order_id
                )

                if not order_items:
                    raise NotUserOrder()

                return order_items

            except NotUserOrder:
                return []

            except Exception:
                logger.exception(
                    "Ошибка выдачи заказа=%s пользователю=%s", order_id, telegram_id
                )
                return []


order_service = OrderService()
