from typing import List

from sqlalchemy import delete, func, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Basket, BasketItem, Product
from app.schemas.schema import OrderInfoItem, ProductsInBasket


class BasketRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_basket(self, telegram_id: int):
        await self.session.execute(insert(Basket).values(telegram_id=telegram_id))

    async def get_or_create_active_basket(self, telegram_id: int):
        result = await self.session.execute(
            select(Basket).where(
                Basket.telegram_id == telegram_id,
            )
        )

        basket = result.scalar_one_or_none()

        if basket is not None:
            return basket

        basket = Basket(telegram_id=telegram_id)
        self.session.add(basket)

        return basket

    async def get_product_quantity_in_active_basket(
        self, telegram_id: int, product_id: int
    ) -> int:
        basket = await self.get_or_create_active_basket(telegram_id)
        if basket is None:
            return 0

        result = await self.session.execute(
            select(BasketItem.quantity).where(
                BasketItem.basket_id == basket.id,
                BasketItem.product_id == product_id,
            )
        )

        quantity = result.scalar_one_or_none()
        return int(quantity or 0)

    async def get_active_basket_total_price(self, telegram_id: int) -> int:
        result = await self.session.execute(
            select(
                func.coalesce(
                    func.sum(BasketItem.quantity * BasketItem.price_at_time), 0
                )
            )
            .join(Basket, BasketItem.basket_id == Basket.id)
            .where(
                Basket.telegram_id == telegram_id,
            )
        )
        total_price = result.scalar_one()
        return int(total_price)

    async def clear_basket(self, basket_id: int):
        await self.session.execute(
            delete(BasketItem).where(BasketItem.basket_id == basket_id)
        )

    async def get_basket_id_by_id(self, telegram_id: int):
        result = await self.session.execute(
            select(Basket.id).where(
                Basket.telegram_id == telegram_id,
            )
        )

        return result.scalar_one_or_none()

    async def add_product(
        self, basket_id: int, product_id: int, price: int, quantity: int
    ) -> None:
        """Добавляем товар в корзину пользователя с проверкой на наличие такого же товара"""
        result = await self.session.execute(
            select(BasketItem).where(
                BasketItem.basket_id == basket_id,
                BasketItem.product_id == product_id,
            )
        )

        basket_item = result.scalar_one_or_none()

        if basket_item is not None:
            basket_item.quantity += quantity
            basket_item.price_at_time = price
            return

        basket_item = BasketItem(
            basket_id=basket_id,
            product_id=product_id,
            quantity=quantity,
            price_at_time=price,
        )

        self.session.add(basket_item)

    async def remove_product(self, basket_id: int, product_id: int) -> None:
        await self.session.execute(
            delete(BasketItem).where(
                BasketItem.basket_id == basket_id,
                BasketItem.product_id == product_id,
            )
        )

    async def get_basket_summary(self, telegram_id: int) -> List[OrderInfoItem]:
        result = await self.session.execute(
            select(
                Product.name,
                BasketItem.quantity,
                BasketItem.price_at_time,
            )
            .join(BasketItem, BasketItem.product_id == Product.id)
            .join(Basket, Basket.id == BasketItem.basket_id)
            .where(
                Basket.telegram_id == telegram_id,
            )
        )

        return [
            OrderInfoItem(
                name=name,
                quantity=quantity,
                price=price)
            for name, quantity, price in result.all()
        ]

    async def get_basket_products(self, basket_id: int):
        result = await self.session.execute(
            select(BasketItem).where(
                BasketItem.basket_id == basket_id,
            )
        )

        return result.scalars().all()

    async def get_basket_summary_with_id(
        self, telegram_id: int
    ) -> list[tuple[str, int, int, int]]:
        result = await self.session.execute(
            select(
                Product.name,
                Product.id,
                BasketItem.quantity,
                BasketItem.price_at_time,
            )
            .join(BasketItem, BasketItem.product_id == Product.id)
            .join(Basket, Basket.id == BasketItem.basket_id)
            .where(
                Basket.telegram_id == telegram_id,
            )
        )

        return [
            (name, product_id, quantity, price)
            for name, product_id, quantity, price in result.all()
        ]

    async def get_active_basket_total_price_by_basket(self, basket_id: int) -> int:
        result = await self.session.execute(
            select(
                func.coalesce(
                    func.sum(BasketItem.quantity * BasketItem.price_at_time), 0
                )
            ).where(
                BasketItem.basket_id == basket_id,
            )
        )

        total_price = result.scalar_one()
        return int(total_price)

    async def get_products_in_basket(self, telegram_id: int) -> List[ProductsInBasket]:
        result = await self.session.execute(
            select(
                Product.id,
                Product.name,
                BasketItem.quantity,
            )
            .join(BasketItem, BasketItem.product_id == Product.id)
            .join(Basket, Basket.id == BasketItem.basket_id)
            .where(Basket.telegram_id == telegram_id)
        )

        return [
            ProductsInBasket(
                product_id=product.id,
                name=product.name,
                quantity=product.quantity,
            )
            for product in result.all()
        ]

    async def get_total_price_by_product_id(
        self, telegram_id: int, product_id: int
    ) -> int:
        result = await self.session.execute(
            select(BasketItem.quantity * BasketItem.price_at_time)
            .join(Basket)
            .where(
                Basket.telegram_id == telegram_id,
                BasketItem.product_id == product_id,
            )
        )

        total_price = result.scalar_one_or_none()
        return total_price or 0

    async def get_basket_product_info(self, telegram_id: int, product_id: int) -> OrderInfoItem:
        result = await self.session.execute(
            select(
                Product.name.label("name"),
                BasketItem.quantity.label("quantity"),
                BasketItem.price_at_time.label("price"),
            )
            .join(Product, BasketItem.product_id == Product.id)
            .join(Basket, BasketItem.basket_id == Basket.id)
            .where(
                BasketItem.product_id == product_id,
                Basket.telegram_id == telegram_id,

            )
        )

        info = result.mappings().one()

        return OrderInfoItem.model_validate(info)

    async def update_product_quantity_in_basket(
        self,
        basket_id: int,
        product_id: int,
        new_quantity: int
    ) -> None:
        await self.session.execute(
            update(BasketItem)
            .values(quantity=new_quantity)
            .where(
                BasketItem.basket_id == basket_id,
                BasketItem.product_id == product_id,
            )
        )