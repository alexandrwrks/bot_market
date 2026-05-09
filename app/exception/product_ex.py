class ProductError(Exception):
    pass

class NotFoundProductError(ProductError):
    pass

class NotEnoughProductQuantityError(ProductError):
    pass


class NoProductsInCategoryError(ProductError):
    # Отсутствие товаров по данной категории
    pass