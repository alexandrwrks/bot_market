from .basket import router as basket_router
from .catalog import router as categories_router
from .orders import router as orders_router
from .start import router as start_router
from .product import router as product_router
# from .test.product_test import router as product_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router,
    product_router,
)
