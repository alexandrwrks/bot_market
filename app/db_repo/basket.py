from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm.config_db import SessionLocal, logger
from app.models.orm.models import Basket, BasketItem, Product


class BasketRepo:
    async def get_or_create_basket(self, telegram_id: int, session: AsyncSession | None = None) -> Basket | None:
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

            return basket

        except IntegrityError as e:
            logger.error(f"Unique error: {e}")
            return None

        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            return None

        finally:
            if own_session:
                await session.close()

    async def add_product_to_basket(self, telegram_id: int, product_id: int, price: int, quantity: int = 1) -> BasketItem | None:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_basket(telegram_id, session=session)
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
                logger.error(f"Database error: {e}")
                return None

    async def get_basket_summary(self, telegram_id: int) -> tuple[list[tuple[str, int, int]], int]:
        async with SessionLocal() as session:
            try:
                basket = await self.get_or_create_basket(telegram_id, session=session)
                if basket is None:
                    return [], 0

                result = await session.execute(
                    select(Product.name, BasketItem.quantity, BasketItem.price_at_time)
                    .join(Product, Product.id == BasketItem.product_id)
                    .where(BasketItem.basket_id == basket.id)
                )
                rows = result.all()
                total = sum(quantity * price for _, quantity, price in rows)
                return rows, total

            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                return [], 0


basket_repo = BasketRepo()
