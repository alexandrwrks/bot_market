from .back import router as back_router
from .basket import router as basket_router
from .categories import router as categories_router
from .orders import router as orders_router
from .start import router as start_router
from app.bot.handler_service.protein import router as protein_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router,
    back_router,
    protein_router,
)
