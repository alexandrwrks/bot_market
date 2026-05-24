from app.database.config import SessionLocal, logger
from app.exception.basket_ex import NotProductsInBasket
from app.exception.order_ex import NotUserOrder, CostEnoughError, CreateOrderError

from app.repo.order_repo import OrderRepo
from app.repo.product_repo import ProductRepo
from app.repo.basket_repo import BasketRepo


class OrderService:
    async def create_order(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
                async with session.begin():
                    basket_repo = BasketRepo(session)
                    order_repo = OrderRepo(session)

                    basket_summary = await basket_repo.get_basket_summary(telegram_id=telegram_id)
                    # basket_summary → [(name, quantity, price)]
                    if not basket_summary:
                        raise NotProductsInBasket()

                    basket_price = await basket_repo.get_active_basket_total_price(telegram_id=telegram_id)
                    if not basket_price:
                        raise NotProductsInBasket()

                    # return basket_summary, basket_price
                    create_order = await order_repo.create_order(
                        telegram_id=telegram_id,
                        total_price=basket_price,
                    )
                    if not create_order:
                        raise CreateOrderError()

                    for name, quantity, price in basket_summary:
                        await order_repo.add_order_item(
                            telegram_id=telegram_id,
                            product_name=name,
                            quantity=quantity,
                            price=price,
                        )


                    """
                    Все товары которые находятся в корзине переместить в таблицу orders
                    из таблицы baskets уделить все товары
                    """

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

    async def check_user_basket_for_order(self, telegram_id: int):
        async with SessionLocal() as session:
            async with session.begin():
                try:
                    basket_repo = BasketRepo(session)

                    basket_price = await basket_repo.get_active_basket_total_price(
                        telegram_id=telegram_id
                    )

                    if basket_price < 5000:
                        raise CostEnoughError()

                    return True

                except Exception:
                    logger.exception(
                        "Ошибка проверки корзины пользователя=%s", telegram_id
                    )
                    raise


order_service = OrderService()
