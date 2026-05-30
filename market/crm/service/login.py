from market.database.config import SessionLocal
from market.repo import CRMRepo
from market.crm.schemas.login import LoginUser


class LoginService:
    async def login(self, user: LoginUser):
        async with SessionLocal() as session:
            user_repo = CRMRepo(session)


login_service = LoginService()
