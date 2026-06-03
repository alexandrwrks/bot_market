from market.database.config import SessionLocal
from market.database.models import Product
from market.utils import logger
from market.bot.exception.product_ex import (
    NotFoundProductError,
    NotEnoughProductQuantityError,
    NoProductsInCategoryError,
)
from market.repo.product_repo import ProductRepo


class ProductService:
    async def get_products_by_category(self, slug: str):
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

    async def get_information_about_product(self, product_id: int):
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)

            async with session.begin():
                try:
                    product = await product_repo.get_product_by_id(product_id)

                    if product is None:
                        raise NotFoundProductError()

                    available = product.quantity

                    if available <= 0:
                        raise NotEnoughProductQuantityError()

                    return product

                except Exception:
                    logger.exception(
                        "Не удалось достать информацию о товаре=%s", product_id
                    )
                    raise NotFoundProductError()

    async def get_product_information(self, product_id: int) -> Product:
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)
            try:
                product = await product_repo.get_product_by_product_id(product_id)
                if not product:
                    raise NotFoundProductError()

                return product

            except Exception as e:
                logger.exception(e)
                raise


product_service = ProductService()
