from market.crm_database import new_session

from market.crm.repo.user_repo import UserRepo


class DashboardService:
    async def get_all_client(self) -> int:
        async with new_session() as session:
            user_repo = UserRepo(session)

            count = await user_repo.get_count_of_clients()
            return count


dashboard_service = DashboardService()
