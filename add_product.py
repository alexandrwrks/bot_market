from app.repo.products import product_repo, NewProduct


import asyncio


async def main():
    """Дбавляю креатин"""
    newProduct = NewProduct(
        category_id=2,
        name="Шоколадный",
        description="Гейнер со вкусом шоколада",
        price=440,
        quantity=20,
        photo_path=r"C:\Users\Acer\OneDrive\Documents\Рабочий стол\Программирование GitHub\bot\bot_market\images\geiner\шоколадный.jpg"
    )

    product = await product_repo.create_product(newProduct)
    if product is None:
        print(f"Ошибка добавления товара")
        return
    
    print(f"Успешное добавление")
    return


if __name__ == "__main__":
    asyncio.run(main())