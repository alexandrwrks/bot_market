class ProductError(Exception):
    pass


class NotFoundProductError(ProductError):
    pass


class NotEnoughProductQuantityError(ProductError):
    # Ошибка: недостаточное количество товара в БД
    pass


class NoProductsInCategoryError(ProductError):
    # Отсутствие товаров по данной категории
    pass
