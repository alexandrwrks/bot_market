from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

from market.crm.config_template import templates
from market.crm.service.dashboard import dashboard_service

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)

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
    data = await dashboard_service.get_details()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "data": data,
        },
        status_code=status.HTTP_200_OK,
    )
