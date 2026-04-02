import os
import logging


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

load_dotenv()

DATA_BASE_NAME = os.getenv("DATA_BASE_NAME")
DATA_BASE_URL = os.getenv("DATA_BASE_URL")

engine = create_async_engine(
    DATA_BASE_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(engine)

Base = declarative_base()

logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


