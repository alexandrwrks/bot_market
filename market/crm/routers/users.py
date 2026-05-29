from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import HTMLResponse

from market.crm.schemas.user import UserSchema
from market.crm.config_template import templates

router = APIRouter(prefix="/users", tags=["users"])

users = [
    {
        "id": 1,
        "name": "Alex",
        "count": 3,
    },
    {
        "id": 2,
        "name": "Bob",
        "count": 1,
    },
    {
        "id": 3,
        "name": "Charlie",
        "count": 0,
    },
    {
        "id": 1,
        "name": "Alex",
        "count": 3,
    },
    {
        "id": 2,
        "name": "Bob",
        "count": 1,
    },
    {
        "id": 3,
        "name": "Charlie",
        "count": 0,
    },
    {
        "id": 1,
        "name": "Alex",
        "count": 3,
    },
    {
        "id": 2,
        "name": "Bob",
        "count": 1,
    },
    {
        "id": 3,
        "name": "Charlie",
        "count": 0,
    },
]


@router.get("/", name="users_page", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    # datas = DashboardData()
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "request": request,
            "users": users,
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
