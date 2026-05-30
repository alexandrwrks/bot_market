import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from market.database import SessionLocal
from market.repo import BasketRepo


async def print_total_price(telegram_id: int, session: AsyncSession):
        basket_repo = BasketRepo(session)
        basket_id = await basket_repo.get_basket_id_by_id(telegram_id)
        total_price = await basket_repo.get_active_basket_total_price_by_basket(basket_id=basket_id)

        return total_price

async def main():
    async with SessionLocal() as session:
        total_price = await print_total_price(telegram_id=id, session=session)

        print(total_price)

        return

id = 1918881124

if __name__ == '__main__':
    asyncio.run(main())