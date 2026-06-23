from typing import List, Tuple

from app.bot.exception.basket_ex import NotProductsInBasket
from app.bot.exception.order_ex import CostEnoughError, CreateOrderError, NotUserOrder
from app.database.config import SessionLocal
from app.repo import BasketRepo, UserRepo
from app.repo.order_repo import OrderRepo
from app.schemas.schema import (
    CreateUserOrderInfo,
    OrderInfo,
    OrderInfoItem,
    UserOrderInfo,
)
from app.utils import logger, settings


class OrderService:
    async def create_order(self, telegram_id: int) -> Tuple[int, int]:
        """
        Создание заказа пользователя

        аргументы функции → telegram_id: int

        План действий:
        1) создать заказ и получить id
        2) перекинуть все продукты с корзины в таблицу OrderItem
        3) вернуть данные о заказе: order_id, total_price,

        """
        try:
            async with SessionLocal() as session:
                order_repo = OrderRepo(session)
                basket_repo = BasketRepo(session)
                user_repo = UserRepo(session)

                async with session.begin():
                    """Создание заказа
                    telegram_id: int,
                    total_price: int → стоимость всего заказа,
                    """
                    user_info = await user_repo.get_user(telegram_id=telegram_id)
                    if user_info is None:
                        raise NotUserOrder()

                    total_price = await basket_repo.get_active_basket_total_price(
                        telegram_id=telegram_id
                    )
                    if total_price == 0 or total_price < settings.MIN_VALUE:
                        logger.warning(
                            "Failed create order basket invalid price: telegram_id=%s",
                            telegram_id,
                        )
                        raise NotProductsInBasket()

                    order_id = await order_repo.create_order(
                        CreateUserOrderInfo(
                            telegram_id=telegram_id,
                            full_name=user_info.full_name,
                            phone=user_info.phone,
                            address=user_info.address,
                            total_price=total_price,
                        )
                    )

                    if order_id is None:
                        logger.warning(
                            "Failed create order: telegram_id=%s", telegram_id
                        )
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
                    telegram_id, full_name, phone, address
                    """
                    basket_id = await basket_repo.get_basket_id_by_id(
                        telegram_id=telegram_id
                    )
                    if not basket_id:
                        raise NotProductsInBasket()

                    await basket_repo.clear_basket(basket_id=basket_id)

                    logger.info(
                        "Successful order creation: telegram_id=%s, order_id=%s",
                        telegram_id,
                        order_id,
                    )
                    return order_id, total_price

        except Exception:
            logger.exception("Ошибка создания заказа: telegram_id=%s", telegram_id)
            raise

    async def get_user_orders(self, telegram_id: int) -> List[UserOrderInfo]:
        """Выдаём все заказы которые есть у пользователя"""
        try:
            async with SessionLocal() as session:
                order_repo = OrderRepo(session)

                orders = await order_repo.get_user_orders_info(telegram_id=telegram_id)
                if not orders:
                    raise NotUserOrder()

                return [
                    UserOrderInfo(
                        id=order.id,
                        total_price=order.total_price,
                        status=order.status,
                        created_at=order.created_at.strftime("%d.%m.%Y %H:%M"),
                    )
                    for order in orders
                ]

        except Exception:
            logger.exception("Ошибка выдачи заказов пользователя=%s", telegram_id)
            raise

    async def check_user_basket_for_order(self, telegram_id: int) -> bool:
        try:
            async with SessionLocal() as session:
                basket_repo = BasketRepo(session)
                async with session.begin():
                    basket_price = await basket_repo.get_active_basket_total_price(
                        telegram_id=telegram_id
                    )

                    if basket_price < 5000:
                        logger.warning(
                            "The user tried to place an order for goods worth less than 5000 RUB: telegram_id=%s",
                            telegram_id,
                        )
                        raise CostEnoughError()

                    return True

        except Exception:
            logger.exception("Ошибка проверки корзины пользователя=%s", telegram_id)
            raise

    async def get_user_order_info(self, order_id: int) -> OrderInfo:
        try:
            async with SessionLocal() as session:
                order_repo = OrderRepo(session)

                order_items = await order_repo.get_order_items(order_id=order_id)
                if not order_items:
                    raise NotUserOrder()

                items = [
                    OrderInfoItem(
                        name=item.product_name,
                        quantity=item.quantity,
                        price=item.price_at_time,
                    )
                    for item in order_items
                ]

                order = await order_repo.get_user_order_info(order_id=order_id)
                if not order:
                    logger.warning("No order information found: order_id=%s", order_id)
                    raise NotUserOrder()

                return OrderInfo(
                    id=order.id,
                    total_price=order.total_price,
                    status=order.status,
                    created_at=order.created_at.strftime("%d.%m.%Y %H:%M"),
                    items=items,
                )

        except Exception:
            logger.exception(
                "Error when receiving the order information: order_id=%s", order_id
            )
            raise


order_service = OrderService()
