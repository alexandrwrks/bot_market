from aiogram.types import User as TgUser

from market.database.config import SessionLocal
from market.utils import logger
from market.bot.exception.user_ex import UserAdminLicense, NotFoundUserError
from market.repo import BasketRepo, order_repo, OrderRepo
from market.repo.user_repo import UserRepo


class UserService:
    async def existing_user(self, user: TgUser):
        async with SessionLocal() as session:
            user_repo = UserRepo(session)
            basket_repo = BasketRepo(session)
            try:
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

                    logger.info("Successful user login in the crm")

                    return True

            except Exception:
                logger.exception("User addition error")
                raise

    async def admin_panel(self, telegram_id: int):
        async with SessionLocal() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                try:
                    user = await user_repo.get_user(telegram_id)
                    if not user:
                        raise NotFoundUserError()

                    if not user.admin:
                        raise UserAdminLicense()

                    return True

                except Exception:
                    logger.exception(
                        "Ошибка инициализации пользователя=%s", telegram_id
                    )
                    raise

    async def get_admin(self, telegram_id: int):
        async with SessionLocal() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                try:
                    await user_repo.update_admin(telegram_id)

                    logger.info(
                        "Успешное добавление админки пользователю=%s", telegram_id
                    )

                except Exception:
                    logger.exception(
                        "Ошибка добавления админки для пользователя=%s", telegram_id
                    )
                    raise

    async def get_all_users(self):
        async with SessionLocal() as session:
            async with session.begin():
                user_repo = UserRepo(session)

                users = await user_repo.get_all_users()

                return users

    async def get_user_details_by_telegram_id(self, telegram_id: int):
        async with SessionLocal() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                order_repo = OrderRepo(session)

                user = await user_repo.get_user(telegram_id)
                count_of_order = await order_repo.get_count_of_order(telegram_id)
                order_cost = await order_repo.get_order_cost(telegram_id)

                return user, count_of_order, order_cost


user_service = UserService()
