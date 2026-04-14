from .Back_hand import router as back_router
from .basket_hand import router as basket_router
from .categoties_hand import router as categories_router
from .fsm import router as fsm_router
from .orders_hand import router as orders_router
from .start_hand import router as start_router
from app.handlers.handler_service.protein import router as protein_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router,
    back_router,
    protein_router,
    fsm_router,
)
