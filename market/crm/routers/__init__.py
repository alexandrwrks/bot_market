from .login import router as login_router
from .users import router as user_router
from .orders import router as order_router
from .dashboards import router as dashboard_router
from .products import router as product_router

handlers = (
    login_router,
    user_router,
    order_router,
    dashboard_router,
    product_router,
)
