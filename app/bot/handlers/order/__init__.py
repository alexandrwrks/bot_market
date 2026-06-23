from app.bot.handlers.order.confirm import router as confirm_router
from app.bot.handlers.order.order_command import router as order_command_router
from app.bot.handlers.order.order_hand import router as order_hand_router

orders_routers = (
    confirm_router,
    order_command_router,
    order_hand_router,
)
