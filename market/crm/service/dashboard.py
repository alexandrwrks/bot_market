from market.crm.schemas import DashboardData
from market.database.config import SessionLocal

from market.repo import CRMRepo, OrderRepo
from market.utils import logger


class DashboardService:
    async def get_all_client(self) -> int:
        async with SessionLocal() as session:
            user_repo = CRMRepo(session)

            count = await user_repo.get_count_of_clients()
            return count

    async def get_details(self):
        async with SessionLocal() as session:
            user_repo = CRMRepo(session)
            order_repo = OrderRepo(session)
            try:
                users = await user_repo.get_count_of_clients()
                orders = await order_repo.get_count_of_orders()
                cost = await order_repo.get_cost_active_orders()

                return DashboardData(
                    count_clients=users, count_deal=orders, count_revenue=cost
                )

            except Exception as e:
                logger.exception("Ошибка", e)
                raise


dashboard_service = DashboardService()
