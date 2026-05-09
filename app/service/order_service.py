from app.database.config import SessionLocal, logger

from app.repo.order_repo import OrderRepo
from app.repo.product_repo import ProductRepo
from app.repo.basket_repo import BasketRepo

class OrderService:
    async def create_order(
            self, telegram_id: int
    ):
        async with SessionLocal() as session:
            try:
                async with session.begin():
                    product_repo = ProductRepo(session)
                    basker_repo = BasketRepo(session)
                    order_repo = OrderRepo(session)

            except Exception as e:
                logger.error(e)
                raise


        