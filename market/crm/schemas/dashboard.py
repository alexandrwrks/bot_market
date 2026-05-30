from pydantic import BaseModel

class DashboardData(BaseModel):
    count_clients: int
    count_deal: int
    count_tasks: int = 4
    count_revenue: int