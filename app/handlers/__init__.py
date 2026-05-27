from .basket_hand import router as basket_router
from .catalog_hand import router as categories_router
from app.handlers.order.order_hand import router as orders_router
from .start_hand import router as start_router
from .product_hand import router as product_router
from .order.order_confirm import router as order_confirm
from .admin_hand import router as admin_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router,
    product_router,
    admin_router,
    order_confirm,
)
