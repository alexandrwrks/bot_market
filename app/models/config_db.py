import os
import logging

from dotenv import load_dotenv

load_dotenv()

DATA_BASE_NAME = os.getenv("DATA_BASE_NAME")

logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)
