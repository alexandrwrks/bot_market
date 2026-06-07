from enum import Enum
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from pydantic import BaseModel

from app.database.config import SessionLocal
from app.repo import OrderRepo, ProductRepo, UserRepo
from app.utils import logger
from app.utils.config import settings


class AdminNotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def notify_new_order(self, order, user) -> None:
        text = (
            "🛒 <b>Новый заказ</b>\n\n"
            f"ID заказа: <code>{order.id}</code>\n"
            f"Пользователь: {user.full_name}\n"
            f"Telegram ID: <code>{user.telegram_id}</code>\n"
            f"Телефон: {order.phone}\n"
            f"Сумма: {order.total_price} ₽"
        )

        for admin_id in settings.ADMIN_IDS:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode="HTML",
                )

            except TelegramAPIError:
                logger.exception("Ошибка отправки сообщений админам")


class AdminInfo(BaseModel):
    users: int
    orders: int


class Status(str, Enum):
    created = "created"
    processing = "processing"
    paid = "paid"


class AdminOrders(BaseModel):
    number: int
    name: str
    phone: str
    total_price: int
    status: Status


class AdminService:
    async def get_admin_info(self) -> AdminInfo:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)
                order_repo = OrderRepo(session)

                users = await user_repo.get_count_users()
                orders = await order_repo.get_count_of_orders()

                logger.info("Successful delivery of admin information")
                return AdminInfo(
                    users=users,
                    orders=orders,
                )

        except Exception:
            logger.exception("Failed to get admin information")
            raise

    async def get_admin_orders(self) -> List[AdminOrders]:
        try:
            async with SessionLocal() as session:
                order_repo = OrderRepo(session)

                orders = await order_repo.get_active_users_orders()

                logger.info("Successful delivery of orders")
                return [
                    AdminOrders(
                        number=order.id,  # номер телефона
                        name=order.name,  # имя пользователя
                        phone=order.phone,  # номер телефона
                        total_price=order.total_price,  # стоимость заказа
                        status=Status(order.status),  # статус заказа
                    )
                    for order in orders
                ]

        except Exception:
            logger.exception("Failed to get admin orders")
            raise

    async def set_access_price(self, product_id: int, new_price: int) -> None:
        try:
            async with SessionLocal() as session:
                product_repo = ProductRepo(session)
                async with session.begin():
                    await product_repo.update_product_price(
                        product_id=product_id, new_price=new_price
                    )
                    logger.info(
                        "Updated product price: product_id=%s, new_price=%s",
                        product_id,
                        new_price,
                    )

        except Exception:
            logger.exception(
                "Failed to update product price: product_id=%s, new_price=%s",
                product_id,
                new_price,
            )
            raise

    async def set_access_quantity(self, product_id: int, new_quantity: int) -> None:
        try:
            async with SessionLocal() as session:
                product_repo = ProductRepo(session)
                async with session.begin():
                    await product_repo.update_product_quantiy(
                        product_id=product_id, new_quantity=new_quantity
                    )
                    logger.info(
                        "Updated product quantity: product_id=%s, new_quantity=%s",
                        product_id,
                        new_quantity,
                    )

        except Exception:
            logger.exception(
                "Failed to update product quantity: product_id=%s, new_quantity=%s",
                product_id,
                new_quantity,
            )
            raise

    async def delete_product(self, product_id: int) -> None:
        try:
            async with SessionLocal() as session:
                product_repo = ProductRepo(session)
                async with session.begin():
                    product_name = await product_repo.soft_product_delete(product_id)
                    logger.info(
                        "Successful product delete: product_id=%s, product_name=%s",
                        product_id, product_name
                    )

                    return product_name

        except Exception:
            logger.exception("Failed to delete product: product_id=%s", product_id)
            raise


admin_service = AdminService()
