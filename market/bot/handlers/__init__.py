from market.bot.handlers.order.order_hand import router as orders_router
from market.bot.handlers.admin_hand import router as admin_router
from market.bot.handlers.basket_hand import router as basket_router
from market.bot.handlers.catalog_hand import router as categories_router
from market.bot.handlers.order.order_confirm import router as order_confirm
from market.bot.handlers.product_hand import router as product_router
from market.bot.handlers.start_hand import router as start_router

routers = (
    start_router,
    basket_router,
    categories_router,
    orders_router,
    product_router,
    admin_router,
    order_confirm,
)
