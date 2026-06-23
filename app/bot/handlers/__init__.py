from app.bot.handlers.basket_hand import router as basket_router
from app.bot.handlers.catalog_hand import router as categories_router
from app.bot.handlers.product_hand import router as product_router
from app.bot.handlers.start_hand import router as start_router

from app.bot.handlers.admin_routers import admin_routers
from app.bot.handlers.order import orders_routers as orders_routers

routers = (
    *admin_routers,
    start_router,
    basket_router,
    categories_router,
    product_router,
    *orders_routers,
)
