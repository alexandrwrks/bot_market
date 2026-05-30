import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(
            filename="crm_market.log",
            encoding="utf-8",
        )
    ],
)

logger = logging.getLogger(__name__)
