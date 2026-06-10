from typing import List, Tuple

from aiogram.types import User as TgUser

from app.bot.exception.user_ex import NotFoundUserError, UserAdminLicense
from app.bot.fsm.order_fsm import OrderCreateSchema
from app.database.config import SessionLocal
from app.database.models import User
from app.repo import BasketRepo, OrderRepo
from app.repo.user_repo import UserRepo
from app.utils import logger


class UserService:
    async def existing_user(self, user: TgUser) -> bool:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)
                basket_repo = BasketRepo(session)

                async with session.begin():
                    """
                    Проверяем наличие пользователя:
                    если пользователь нет → создаём запись в users и baskets,
                    если есть, то возращаем что пользователь есть и можно без проблем продолжать
                    """
                    user_exists = await user_repo.get_user(user.id)
                    if user_exists is None:
                        await user_repo.create_user(user)
                        await basket_repo.create_basket(user.id)
                        logger.info(
                            "Successful user registration: telegram_id=%s", user.id
                        )

                    return True

        except Exception:
            logger.exception("User addition error")
            raise

    async def admin_panel(self, telegram_id: int) -> bool:
        try:
            async with SessionLocal() as session:
                async with session.begin():
                    user_repo = UserRepo(session)

                    user = await user_repo.get_user(telegram_id)
                    if not user:
                        raise NotFoundUserError()

                    if not user.admin:
                        raise UserAdminLicense()

                    return True

        except Exception:
            logger.exception("Ошибка инициализации пользователя=%s", telegram_id)
            raise

    async def get_admin(self, telegram_id: int) -> None:
        try:
            async with SessionLocal() as session:
                async with session.begin():
                    user_repo = UserRepo(session)

                    await user_repo.update_admin(telegram_id)

                    logger.info(
                        "Успешное добавление админки пользователю=%s", telegram_id
                    )

        except Exception:
            logger.exception(
                "Ошибка добавления админки для пользователя=%s", telegram_id
            )
            raise

    async def get_all_users(self) -> List[User]:
        async with SessionLocal() as session:
            async with session.begin():
                user_repo = UserRepo(session)

                users = await user_repo.get_all_users()

                return users

    async def get_user_details_by_telegram_id(
        self, telegram_id: int
    ) -> Tuple[User, int, int]:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)
                order_repo = OrderRepo(session)
                async with session.begin():
                    user = await user_repo.get_user(telegram_id)
                    count_of_order = await order_repo.get_count_of_order(telegram_id)
                    order_cost = await order_repo.get_order_cost(telegram_id)

                    return user, count_of_order, order_cost

        except Exception:
            logger.exception("Failed to get user details")
            raise

    async def get_user_info_for_order(self, telegram_id: int) -> OrderCreateSchema:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)

                user_info = await user_repo.get_user(telegram_id)

                return OrderCreateSchema(
                    address=user_info.address,
                    full_name=user_info.full_name,
                    phone=user_info.phone
                )

        except Exception:
            logger.exception("Failed to get order info")
            raise


    async def update_user_address(self, address: str, telegram_id: int) -> OrderCreateSchema:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)
                async with session.begin():
                    order = await user_repo.update_user_address(address, telegram_id)

                    logger.info("Успешное обновление адреса: telegram_id=%s", telegram_id)
                    return order

        except Exception:
            logger.exception("Failed to update address user information")
            raise

    async def update_user_full_name(self, full_name: str, telegram_id: int) -> OrderCreateSchema:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)
                async with session.begin():
                    order = await user_repo.update_user_full_name(full_name, telegram_id)

                    logger.info("Успешное обновление ФИО: telegram_id=%s", telegram_id)
                    return order

        except Exception:
            logger.exception("Failed to update full_name user information")
            raise

    async def update_user_phone(self, phone: str, telegram_id: int) -> OrderCreateSchema:
        try:
            async with SessionLocal() as session:
                user_repo = UserRepo(session)
                async with session.begin():
                    order = await user_repo.update_user_phone(phone, telegram_id)

                    logger.info("Успешное обновление телефон: telegram_id=%s", telegram_id)
                    return order

        except Exception:
            logger.exception("Failed to update phone user information")
            raise



user_service = UserService()
