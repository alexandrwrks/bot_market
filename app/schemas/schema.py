from pydantic import BaseModel


class UserOrderInfo(BaseModel):
    id: int
    total_price: int
    status: str
    created_at: str


class OrderInfoItem(BaseModel):
    name: str
    quantity: int
    price: int

    @property
    def total(self) -> int:
        return self.quantity * self.price


class OrderInfo(BaseModel):
    id: int
    total_price: int
    status: str
    created_at: str
    items: list[OrderInfoItem]


class ProductsInBasket(BaseModel):
    product_id: int
    name: str
    quantity: int

class CategoryCreate(BaseModel):
    name: str
    slug: str