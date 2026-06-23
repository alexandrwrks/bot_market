from typing import List

from app.bot.exception.product_ex import (
    NoProductsInCategoryError,
    NotEnoughProductQuantityError,
    NotFoundProductError,
)
from app.database.config import SessionLocal
from app.database.models import Product
from app.repo.product_repo import ProductRepo
from app.utils import logger


class ProductService:
    async def get_products_by_category(self, slug: str) -> List[Product]:
        """
        router -> category:
        Показываем все доступные товары по выбранной категории
        """
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)

            products = await product_repo.get_products_by_slug(slug)
            if not products:
                raise NoProductsInCategoryError()

            logger.info(f"Успешное получение товаров по категории {slug}")

            return products

    async def get_information_about_product(self, product_id: int) -> Product:
        try:
            async with SessionLocal() as session:
                product_repo = ProductRepo(session)
                async with session.begin():
                    product = await product_repo.get_product_by_id(product_id)

                    if product is None:
                        raise NotFoundProductError()

                    available = product.quantity

                    if available <= 0:
                        raise NotEnoughProductQuantityError()

                    return product

        except Exception:
            logger.exception("Не удалось достать информацию о товаре=%s", product_id)
            raise

    async def get_product_information(self, product_id: int) -> Product:
        try:
            async with SessionLocal() as session:
                product_repo = ProductRepo(session)

                product = await product_repo.get_product_by_product_id(product_id)
                if not product:
                    raise NotFoundProductError()

                return product

        except Exception as e:
            logger.exception(e)
            raise


product_service = ProductService()
