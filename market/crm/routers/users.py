from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import HTMLResponse

from market.bot.service.user_service import user_service
from market.crm.config_template import templates


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", name="users_page", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    users = await user_service.get_all_users()
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "request": request,
            "users": users,
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/telegram/{user_id}", name="user_page", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    (
        user,
        count_of_order,
        order_cost,
    ) = await user_service.get_user_details_by_telegram_id(user_id)

    if user:
        return templates.TemplateResponse(
            request=request,
            name="user.html",
            context={
                "request": request,
                "user": user,
                "count_of_order": count_of_order,
                "order_cost": order_cost,
            },
            status_code=status.HTTP_200_OK,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
