from .product_update.price import router as price_router
from .product_update.quantity import router as quantity_router

__all__ = [
    "price_router",
    "quantity_router",
]
