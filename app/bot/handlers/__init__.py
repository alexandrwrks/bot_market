from app.bot.handlers.admin_hand import router as admin_router
from app.bot.handlers.admin_routers import price_router as admin_product_router
from app.bot.handlers.admin_routers import quantity_router
from app.bot.handlers.admin_routers.add_category import \
    router as add_category_router
from app.bot.handlers.admin_routers.add_product import \
    router as add_product_router
from app.bot.handlers.basket_hand import router as basket_router
from app.bot.handlers.catalog_hand import router as categories_router
from app.bot.handlers.order.order_confirm import router as order_confirm
from app.bot.handlers.order.order_hand import router as orders_router
from app.bot.handlers.product_hand import router as product_router
from app.bot.handlers.start_hand import router as start_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router,
    product_router,
    admin_router,
    order_confirm,
    admin_product_router,
    quantity_router,
    add_product_router,
    add_category_router
)
