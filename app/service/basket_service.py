from app.repo.basket import basket_repo
from app.repo.products import product_repo

import asyncio

class BasketService:
    def __init__(self):
        pass

    async def add_product_basket(self, product_id: int, quantity: int, telegram_id: int) -> None:
        """Уменьшаем количество в БД и добавляем товар в корзину пользователя"""
        product = await product_repo.get_product_by_id(product_id)
        price = product.price

        await asyncio.gather(
            basket_repo.add_product_to_basket(
                product_id=product_id,
                price=price,
                quantity=quantity,
                telegram_id=telegram_id,
            ),
            product_repo.update_product_quantity(
                product_id=product_id,
                quantity=quantity
            )
        )

    async def remove_product_from_basket(self, product_id: int, telegram_id: int) -> None:
        """Уменьшение количества товара с корзины и добавления товара в БД"""
        product_quantity = await  basket_repo.get_product_quantity_in_active_basket(
            telegram_id=telegram_id,
            product_id=product_id
        ) # Получаем количество товара в корзине пользователя

        await asyncio.gather(
            product_repo.add_product_quantity(
                product_id=product_id,
                quantity=product_quantity
            ),

        )

