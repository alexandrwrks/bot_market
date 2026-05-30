from market.crm_database import new_session
from market.crm.repo.user_repo import UserRepo
from market.crm.schemas.login import LoginUser


class LoginService:
    async def login(self, user: LoginUser):
        async with new_session() as session:
            user_repo = UserRepo(session)


login_service = LoginService()
