from market.database.config import SessionLocal

from market.repo import CRMRepo


class DashboardService:
    async def get_all_client(self) -> int:
        async with SessionLocal() as session:
            user_repo = CRMRepo(session)

            count = await user_repo.get_count_of_clients()
            return count


dashboard_service = DashboardService()
