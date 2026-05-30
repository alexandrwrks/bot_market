from market.database.config import SessionLocal
from market.repo import ProductRepo


class ProductsService:
    async def get_all_products(self):
        async with SessionLocal() as session:
            products_repo = ProductRepo(session)

            products = await products_repo.get_all_products()

            return products


products_service = ProductsService()
