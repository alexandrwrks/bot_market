from sqlalchemy.util import await_only

from app.database.config import SessionLocal, logger
from app.exception.product_ex import NotFoundProductError, NotEnoughProductQuantityError, NoProductsInCategoryError
from app.repo.basket_repo import BasketRepo
from app.repo.product_repo import ProductRepo


class ProductService:
    async def get_products_by_category(
            self, slug: str,
    ):
        """
        router -> category:
        Показываем все доступные товары по выбранной категории
        """
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)

            products = await product_repo.get_products_by_slug(slug)
            if products is None:
                raise NoProductsInCategoryError()

            logger.info("Успешное получение товаров по категории")

            return products

    async def get_information_about_product(
            self, product_id: int
    ):
        async with SessionLocal() as session:
            product_repo = ProductRepo(session)
            basket_repo = BasketRepo(session)

            async with session.begin():
                try:
                    product = await product_repo.get_product_by_id(product_id)

                    if not product:
                        raise NotFoundProductError()

                    available = product.quantity

                    if available <= 0:
                        raise NotEnoughProductQuantityError()

                    return product

                except Exception:
                    await session.rollback()
                    logger.exception(
                        "Не удалось достать информацию о товаре=%s",
                        product_id
                    )


product_service = ProductService()