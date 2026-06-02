from pydantic import BaseModel


class UserOrderInfo(BaseModel):
    id: int
    total_price: int
    status: str
    created_at: str