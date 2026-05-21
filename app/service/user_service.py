from app.database.config import SessionLocal, logger

from app.repo.user_repo import UserRepo

from app.exception.user_ex import UserAdminLicense, NotFoundUserError


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
                logger.exception("Ошибка добавления пользователя=%s", telegram_id)

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

    async def get_admin(self, telegrm_id: int):
        async with SessionLocal() as session:
            async with session.begin():
                try:
                    user_repo = UserRepo(session)

                    await user_repo.update_admin(telegrm_id)

                    logger.info(
                        "Успешное добавление админки пользователю=%s",
                        telegrm_id
                    )

                except Exception:
                    logger.exception(
                        "Ошибка добавления админки для пользователя=%s",
                        telegrm_id
                    )



user_service = UserService()
