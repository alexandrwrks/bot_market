from typing import Optional

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import SessionLocal, logger
from app.database.models import Basket, BasketItem, Product


class BasketRepo:
    async def get_or_create_active_basket(
        self,
        telegram_id: int,
        session: AsyncSession | None = None,
    ) -> Optional[Basket]:
        own_session = session is None
        session = session or SessionLocal()

        try:
            result = await session.execute(
                select(Basket).where(
                    Basket.telegram_id == telegram_id,
                    Basket.status == "active",
                )
            )
            basket = result.scalar_one_or_none()

            if basket is not None:
                return basket

            basket = Basket(telegram_id=telegram_id, status="active")
            session.add(basket)

            if own_session:
                await session.commit()
                await session.refresh(basket)
            else:
                await session.flush()

            return basket

        except SQLAlchemyError as e:
            logger.error(f"Basket get/create error: {e}")
            return None

        finally:
            if own_session:
                await session.close()

    async def get_active_user_basket(self, telegram_id: int) -> list[tuple[str, int, int]]:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_active_basket(telegram_id, session=session)
                if basket is None:
                    return []

                result = await session.execute(
                    select(Product.name, BasketItem.quantity, BasketItem.price_at_time)
                    .join(Product, Product.id == BasketItem.product_id)
                    .where(BasketItem.basket_id == basket.id)
                )
                return result.all()

            except SQLAlchemyError as e:
                logger.error(f"Basket items read error: {e}")
                return []

    async def add_product_to_basket(
        self,
        telegram_id: int,
        product_id: int,
        price: int,
        quantity: int,
    ) -> Optional[BasketItem]:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_active_basket(telegram_id, session=session)
                if basket is None:
                    return None

                result = await session.execute(
                    select(BasketItem).where(
                        BasketItem.basket_id == basket.id,
                        BasketItem.product_id == product_id,
                    )
                )
                basket_item = result.scalar_one_or_none()

                if basket_item is not None:
                    basket_item.quantity += quantity
                    await session.commit()
                    await session.refresh(basket_item)
                    return basket_item

                basket_item = BasketItem(
                    basket_id=basket.id,
                    product_id=product_id,
                    quantity=quantity,
                    price_at_time=price,
                )
                session.add(basket_item)

                await session.commit()
                await session.refresh(basket_item)
                return basket_item

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Basket add error: {e}")
                return None

    async def get_product_quantity_in_active_basket(self, telegram_id: int, product_id: int) -> int:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_active_basket(telegram_id, session=session)
                if basket is None:
                    return 0

                result = await session.execute(
                    select(BasketItem.quantity)
                    .where(
                        BasketItem.basket_id == basket.id,
                        BasketItem.product_id == product_id,
                    )
                )
                quantity = result.scalar_one_or_none()
                return int(quantity or 0)

            except SQLAlchemyError as e:
                logger.error(f"Basket quantity read error: {e}")
                return 0

    async def get_active_basket_total_price(self, telegram_id: int) -> int:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_active_basket(telegram_id, session=session)
                if basket is None:
                    return 0

                result = await session.execute(
                    select(func.coalesce(func.sum(BasketItem.quantity * BasketItem.price_at_time), 0)).where(
                        BasketItem.basket_id == basket.id
                    )
                )
                total_price = result.scalar_one()
                return int(total_price)

            except SQLAlchemyError as e:
                logger.error(f"Basket total read error: {e}")
                return 0

    async def clear_basket(self, telegram_id: int) -> bool:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_active_basket(telegram_id, session=session)
                if basket is None:
                    return False

                result = await session.execute(
                    delete(BasketItem).where(BasketItem.basket_id == basket.id)
                )
                await session.commit()
                return (result.rowcount or 0) > 0

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Basket clear error: {e}")
                return False


basket_repo = BasketRepo()
