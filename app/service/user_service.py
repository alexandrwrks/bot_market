from app.database.config import SessionLocal, logger

from app.repo.user_repo import UserRepo


class UserService:
    async def existing_user(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
                async with session.begin():
                    user_repo = UserRepo(session)

                    exist_user = await user_repo.get_user(telegram_id)
                    if exist_user is None:
                        await user_repo.create_user(telegram_id)

            except Exception:
                logger.exception(
                    "Ошибка добавления пользователя=%s",
                    telegram_id
                )

user_service = UserService()