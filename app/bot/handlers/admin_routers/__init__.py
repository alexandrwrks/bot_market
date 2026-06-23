from app.bot.handlers.admin_routers.admin_rout import router as main_admin_router
from app.bot.handlers.admin_routers.category import router as category
from app.bot.handlers.admin_routers.price import router as price
from app.bot.handlers.admin_routers.product import router as product
from app.bot.handlers.admin_routers.quantity import router as quantity

admin_routers = (
    main_admin_router,
    quantity,
    price,
    category,
    product,
)
