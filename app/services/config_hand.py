from app.handlers.start_hand import router as start_router
from app.handlers.basket_hand import router as basket_router
from app.handlers.categoties_hand import router as categories_router
from app.handlers.orders_hand import router as orders_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router
)