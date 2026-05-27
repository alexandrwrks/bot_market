import asyncio

from app.repo.basket_repo import BasketRepo
from app.database.config import SessionLocal

tg_id = 1918881124

async def main(tg_id: int):
    async with SessionLocal() as session:
        basket_repo = BasketRepo(session)

        basket_id = await basket_repo.get_basket_id_by_id(tg_id)

        if basket_id is None:
            print("Нет basket_id")
        else:
            print("basket_id=%s" % basket_id)

        total_price = await basket_repo.get_active_basket_total_price(tg_id)

        if total_price is None:
            print("basket_items отсутствуют")
        else:
            print("total_price=%s" % total_price)



if __name__ == '__main__':
    asyncio.run(main(tg_id))