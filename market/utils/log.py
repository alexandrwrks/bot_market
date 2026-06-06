import logging
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s | %(levelname)s |  %(name)s |  %(message)s"),
    handlers=[
        logging.FileHandler(
            filename="crm_market.log",
            encoding="utf-8",
        )
    ],
)

logger = logging.getLogger(__name__)


def log_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except Exception:
            logger.exception(
                "Error in %s",
                func.__name__,
            )
            raise

    return wrapper
