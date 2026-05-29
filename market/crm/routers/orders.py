from fastapi import APIRouter, status, HTTPException
from sqlalchemy.testing.pickleable import User

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

orders = [
    {"id": 1, "user_id": 1, "count_of_items": 5},
    {"id": 2, "user_id": 2, "count_of_items": 3},
    {"id": 3, "user_id": 3, "count_of_items": 6},
]


@router.get("")
async def get_orders():
    return orders


@router.get("/{id}")
async def get_order(id: int):
    for order in orders:
        if order["id"] == id:
            return order

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
