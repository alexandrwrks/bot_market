from enum import Enum

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from typing import List
from market.bot.exception.admin_ex import AdminInfoError
from market.database.config import SessionLocal
from market.repo import UserRepo, OrderRepo, ProductRepo
from market.utils.config import settings
from market.utils import logger

from pydantic import BaseModel


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
        async with SessionLocal() as session:
            user_repo = UserRepo(session)
            order_repo = OrderRepo(session)
            try:
                users = await user_repo.get_count_users()
                orders = await order_repo.get_count_of_orders()

                return AdminInfo(
                    users=users,
                    orders=orders,
                )

            except Exception as e:
                logger.exception(e)
                raise

    async def get_admin_orders(self) -> List[AdminOrders]:
        async with SessionLocal() as session:
            order_repo = OrderRepo(session)
            try:
                orders = await order_repo.get_active_users_orders()

                lst_orders = []
                for order in orders:
                    lst_orders.append(
                        AdminOrders(
                            number=order.id,  # номер телефона
                            name=order.name,  # имя пользователя
                            phone=order.phone,  # номер телефона
                            total_price=order.total_price,  # стоимость заказа
                            status=Status(order.status),  # статус заказа
                        )
                    )

                return lst_orders

            except Exception as e:
                logger.exception(e)
                raise

    async def set_access_price(self, product_id: int, new_price: int) -> None:
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)
            async with session.begin():
                try:
                    await product_repo.update_product_price(
                        product_id=product_id, new_price=new_price
                    )

                except Exception as e:
                    logger.exception(e)
                    raise

    async def set_access_quantity(self, product_id: int, new_quantity: int) -> None:
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)
            async with session.begin():
                try:
                    await product_repo.update_product_quantiy(product_id=product_id, new_quantity=new_quantity)

                except Exception as e:
                    logger.exception(e)
                    raise

admin_service = AdminService()
