from market.bot.database.config import SessionLocal, logger
from market.bot.exception.basket_ex import NotProductsInBasket
from market.bot.exception.order_ex import (
    NotUserOrder,
    CostEnoughError,
    CreateOrderError,
)
from market.bot.repo.basket_repo import BasketRepo
from market.bot.repo.order_repo import OrderRepo


class OrderService:
    async def create_order(self, telegram_id: int, user_data: dict):
        async with SessionLocal() as session:
            order_repo = OrderRepo(session)
            basket_repo = BasketRepo(session)
            try:
                async with session.begin():
                    """Создание заказа
                    telegram_id: int,
                    total_price: int → стоимость всего заказа,
                    """
                    total_price = await basket_repo.get_active_basket_total_price(
                        telegram_id=telegram_id
                    )
                    if total_price == 0:
                        raise NotProductsInBasket()

                    order_id = await order_repo.create_order(
                        telegram_id=telegram_id,
                        name=user_data["name"],
                        phone=user_data["phone"],
                        total_price=total_price,
                    )
                    if order_id is None:
                        raise CreateOrderError()
                    """
                    Получить все товары находящиеся в корзине пользователя
                    Добавить все товары в таблицу OrderItem
                    """
                    basket_summary = await basket_repo.get_basket_summary_with_id(
                        telegram_id=telegram_id
                    )
                    for name, product_id, quantity, price in basket_summary:
                        await order_repo.add_order_item(
                            order_id=order_id,
                            product_name=name,
                            product_id=product_id,
                            quantity=quantity,
                            price=price,
                        )
                    """
                    Сохраняем данные о пользователе в таблицу OrderInfo
                    user_data: dict → 
                    telegram_id, username, name, surname, phone, email, city, address
                    """
                    basket_id = await basket_repo.get_basket_id_by_id(
                        telegram_id=telegram_id
                    )
                    if not basket_id:
                        raise NotProductsInBasket()

                    await basket_repo.clear_basket(basket_id=basket_id)

                    logger.info(
                        "Успешное создание заказа. Номер заказа=%s, пользователь=%s",
                        order_id,
                        user_data["name"],
                    )
                    return True

            except Exception:
                logger.exception("Ошибка создания заказа")
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
