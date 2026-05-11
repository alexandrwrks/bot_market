from app.repo.basket_repo import BasketRepo
from app.repo.product_repo import ProductRepo

from app.database.config import SessionLocal, logger

from app.exception.basket_ex import (
    AddProductToBasketError,
    NotEnoughProductQuantityError,
    NotProductsInBasket,
    RemoveProductFromBasket,
)
from app.exception.product_ex import NotFoundProductError

from app.exception.user_ex import NotFoundUserError

from dataclasses import dataclass


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
                raise NotFoundProductError()

            in_cart = await basket_repo.get_product_quantity_in_active_basket(
                telegram_id=telegram_id, product_id=product_id
            )

            available = product.quantity - in_cart

            if available <= 0:
                raise NotEnoughProductQuantityError()

            return ProductCartInfo(
                name=product.name,
                available=available,
            )

    async def add_product_to_basket(
        self, telegram_id: int, product_id: int, quantity: int
    ):
        async with SessionLocal() as session:
            try:
                async with session.begin():
                    basket_repo = BasketRepo(session)
                    product_repo = ProductRepo(session)

                    basket = await basket_repo.get_or_create_active_basket(telegram_id)
                    # if basket_id is None:
                    #     raise NotFoundUserError()

                    product = await product_repo.get_product_by_id(product_id)
                    if product is None:
                        raise NotFoundProductError()

                    if product.quantity < quantity:
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
                    "Пользователь %s добавил товар %s, %s шт.",
                    telegram_id,
                    product_id,
                    quantity,
                )

            except (NotFoundProductError, NotEnoughProductQuantityError):
                raise

            except Exception:
                logger.exception(
                    "Не удалось добавить товары в корзину: telegram_id=%s, product_id=%s, quantity=%s",
                    telegram_id,
                    product_id,
                    quantity,
                )
                raise AddProductToBasketError()

    async def remove_product_from_basket(self, telegram_id: int, product_id: int):
        """Полностью убираю товар с корзины пользователя с id=product_id"""
        async with SessionLocal() as session:
            try:
                async with session.begin():
                    basket_repo = BasketRepo(session)
                    product_repo = ProductRepo(session)

                    basket_id = await basket_repo.get_basket_id_by_id(telegram_id)
                    if basket_id is None:
                        raise NotFoundUserError()

                    quantity_in_basket = (
                        await basket_repo.get_product_quantity_in_active_basket(
                            telegram_id=telegram_id, product_id=product_id
                        )
                    )

                    if quantity_in_basket == 0:
                        raise NotProductsInBasket()

                    await basket_repo.remove_product(basket_id, product_id)
                    await product_repo.add_quantity(
                        product_id=product_id, quantity=quantity_in_basket
                    )

            except Exception:
                logger.exception(
                    "Не удалось убрать товар из корзины пользователя: telegram_id=%s, product_id=%s",
                    telegram_id,
                    product_id,
                )
                raise RemoveProductFromBasket()

    async def clear_basket(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
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
                        "Корзина пользователя=%s была успешна удалена", telegram_id
                    )

            except Exception:
                logger.exception(
                    "Не удалось очистить корзину пользователя: telegram_id=%s",
                    telegram_id,
                )
                raise

    async def render_user_basket(self, telegram_id: int):
        async with SessionLocal() as session:
            try:
                basket_repo = BasketRepo(session)

                items = await basket_repo.get_basket_summary(telegram_id)

                if items is None:
                    raise NotFoundProductError()

                total = sum(quantity * price for _, quantity, price in items)

                return items, total

            except Exception:
                logger.exception("Ошибка рендера корзины пользователя=%s", telegram_id)
                return [], 0


basket_service = BasketService()
