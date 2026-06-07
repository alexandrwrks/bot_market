from dataclasses import dataclass
from typing import List, Tuple

from app.bot.exception.basket_ex import (NotEnoughProductQuantityError,
                                         NotProductsInBasket)
from app.bot.exception.product_ex import NotFoundProductError
from app.bot.exception.user_ex import NotFoundUserError
from app.database.config import SessionLocal
from app.repo import BasketRepo
from app.repo.product_repo import ProductRepo
from app.schemas.schema import ProductsInBasket
from app.utils import logger


@dataclass
class ProductCartInfo:
    name: str
    available: int


class BasketService:
    async def get_product_for_cart_input(
        self,
        telegram_id: int,
        product_id: int,
    ) -> ProductCartInfo:
        async with SessionLocal() as session:
            basket_repo = BasketRepo(session)
            product_repo = ProductRepo(session)

            product = await product_repo.get_product_by_id(product_id)

            if product is None:
                logger.warning("The product is out of stock: product_id=%s", product_id)
                raise NotFoundProductError()

            in_cart = await basket_repo.get_product_quantity_in_active_basket(
                telegram_id=telegram_id, product_id=product_id
            )

            available = product.quantity - in_cart

            if available <= 0:
                logger.warning("The product is out of stock: product_id=%s", product_id)
                raise NotEnoughProductQuantityError()

            logger.info(
                "Successful delivery of goods from the basket: telegram_id=%s, product_id=%s",
                telegram_id, product_id
            )
            return ProductCartInfo(
                name=product.name,
                available=available,
            )

    async def add_product_to_basket(
        self, telegram_id: int, product_id: int, quantity: int
    ) -> None:
        try:
            async with SessionLocal() as session:
                async with session.begin():
                    basket_repo = BasketRepo(session)
                    product_repo = ProductRepo(session)

                    basket = await basket_repo.get_or_create_active_basket(telegram_id)

                    product = await product_repo.get_product_by_id(product_id)
                    if product is None:
                        logger.warning(
                            "The product is out of stock: product_id=%s", product_id
                        )
                        raise NotFoundProductError()

                    if product.quantity < quantity:
                        logger.warning(
                            "The product is less than expected: product_id=%",
                            product_id,
                        )
                        raise NotEnoughProductQuantityError()

                    await product_repo.remove_quantity(
                        product_id=product_id, quantity=quantity
                    )

                    await basket_repo.add_product(
                        basket_id=basket.id,
                        product_id=product_id,
                        price=product.price,
                        quantity=quantity,
                    )

                logger.info(
                    "The user_id=%s added the product_id=%s in quantity=%s",
                    telegram_id,
                    product_id,
                    quantity,
                )

        except Exception:
            logger.exception(
                "Не удалось добавить товары в корзину: telegram_id=%s, product_id=%s, quantity=%s",
                telegram_id,
                product_id,
                quantity,
            )
            raise

    async def remove_product_from_basket(
        self, telegram_id: int, product_id: int
    ) -> None:
        """Полностью убираю товар с корзины пользователя с id=product_id"""
        try:
            async with SessionLocal() as session:
                async with session.begin():
                    basket_repo = BasketRepo(session)
                    product_repo = ProductRepo(session)

                    basket_id = await basket_repo.get_basket_id_by_id(telegram_id)
                    if basket_id is None:
                        logger.warning(
                            "User's basket not found: telegram_id=%s", telegram_id
                        )
                        raise NotFoundUserError()

                    quantity_in_basket = (
                        await basket_repo.get_product_quantity_in_active_basket(
                            telegram_id=telegram_id, product_id=product_id
                        )
                    )

                    if quantity_in_basket == 0:
                        logger.warning(
                            "There is no product in the user's cart: telegram_id=%s, product_id=%s",
                            telegram_id,
                            product_id,
                        )
                        raise NotProductsInBasket()

                    await basket_repo.remove_product(basket_id, product_id)
                    await product_repo.add_quantity(
                        product_id=product_id, quantity=quantity_in_basket
                    )

        except Exception:
            logger.exception(
                "Couldn't remove product from user's cart: telegram_id=%s, product_id=%s",
                telegram_id,
                product_id,
            )
            raise

    async def clear_basket(self, telegram_id: int) -> None:
        try:
            async with SessionLocal() as session:
                async with session.begin():
                    basket_repo = BasketRepo(session)
                    product_repo = ProductRepo(session)

                    basket_id = await basket_repo.get_basket_id_by_id(telegram_id)
                    if basket_id is None:
                        raise NotFoundUserError()

                    products = await basket_repo.get_basket_products(basket_id)
                    if not products:
                        raise NotProductsInBasket()

                    for product in products:
                        await product_repo.add_quantity(
                            product_id=product.product_id, quantity=product.quantity
                        )
                    await basket_repo.clear_basket(basket_id)

                    logger.info(
                        "The user's basket has been successfully emptied: telegram_id=%s",
                        telegram_id,
                    )

        except Exception:
            logger.exception(
                "Couldn't empty the user's trash: telegram_id=%s",
                telegram_id,
            )
            raise

    async def render_user_basket(
        self, telegram_id: int
    ) -> Tuple[list[tuple[str, int, int]], int]:
        try:
            async with SessionLocal() as session:
                basket_repo = BasketRepo(session)

                items = await basket_repo.get_basket_summary(telegram_id)
                total = sum(quantity * price for _, quantity, price in items)

                return items, total

        except Exception:
            logger.exception("Basket rendering error: telegram_id=%s", telegram_id)
            raise

    async def get_basket_position(self, telegram_id: int) -> List[ProductsInBasket]:
        try:
            async with SessionLocal() as session:
                basket_repo = BasketRepo(session)

                return await basket_repo.get_products_in_basket(telegram_id=telegram_id)

        except Exception:
            logger.exception(
                "Failed get basket's products: telegram_id=%s", telegram_id
            )
            raise

    async def get_total_price_for_product_in_basket(
        self, telegram_id: int, product_id: int
    ) -> Tuple[int, int]:
        try:
            async with SessionLocal() as session:
                basket_repo = BasketRepo(session)

                quantity = await basket_repo.get_product_quantity_in_active_basket(
                    telegram_id=telegram_id, product_id=product_id
                )
                total_price = await basket_repo.get_total_price_by_product_id(
                    telegram_id=telegram_id, product_id=product_id
                )

                return quantity, total_price

        except Exception:
            logger.exception(
                "Failed get product total price from basket: telegram_id=%s, product_id=%s",
                telegram_id,
                product_id,
            )
            raise


basket_service = BasketService()
