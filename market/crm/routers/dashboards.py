from fastapi import APIRouter, status, Request

from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from market.crm.config_template import templates

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


class DashboardData(BaseModel):
    count_clients: int = 10
    count_deal: int = 3
    count_tasks: int = 4
    count_revenue: int = 140000


# @router.get("/", response_class=HTMLResponse)
# async def client_dashboard(request: Request):
#     count = await dashboard_service.get_all_client()
#     return templates.TemplateResponse(
#         request=request,
#         name="dashboard.html",
#         context={
#             "request": request,
#             "count": count,
#         },
#         status_code=status.HTTP_200_OK
#     )


@router.get("/", name="dashboard_page", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    datas = DashboardData()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "data": datas,
        },
        status_code=status.HTTP_200_OK,
    )
