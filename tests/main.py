import asyncio

from tests.db_test import TestCategpryTable, TestProductTable, Category, Product


test_categories = Category("Протеин", "protein")


test_products1 = Product(1, "Banana-Strawberry Protein 450 gr", "Протеин со вкусомм банана и клубники", 400, r"images\protein\primekraft_protein_banana_strawberry_450.jpg", 10)
test_products2 = Product(1, "Banana-Strawberry Protein 900 gr", "Протеин со вкусомм банана и клубники", 710, r"images\protein\primekraft_protein_banana_strawberry_900.jpg", 5)
test_products3 = Product(1, "Milk Chocolate Protein 900 gr", "Протеин со вкусомм молочного шоколада", 720, r"images\protein\primekraft_protein_chocolate_900.jpg", 7)
test_products4 = Product(1, "Pina Colado Protein 900 gr", "Протеин со вкусомм пина коладо", 700, r"images\protein\primekraft_protein_pina_colado_900.jpg", 8,)


async def main():
    tct = TestCategpryTable()
    tpt = TestProductTable()

    await tct.init_categories_table()
    await tpt.init_products_table()

    await tct.create_category(test_categories)

    await tpt.create_product(test_products1)
    await tpt.create_product(test_products2)
    await tpt.create_product(test_products3)
    await tpt.create_product(test_products4)

if __name__ == "__main__":
    asyncio.run(main())