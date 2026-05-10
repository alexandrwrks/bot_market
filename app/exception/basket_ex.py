class BasketError(Exception):
    # Родительский класс
    pass


class AddProductToBasketError(BasketError):
    # Ошибка: добавления товара в корзину
    pass


class NotFoundProduct(BasketError):
    # Ошибка: не найден товар в корзине
    pass


class NotProductsInBasket(BasketError):
    pass


class RemoveProductFromBasket(BasketError):
    pass


class ClearBasketError(BasketError):
    # Ошибка очистки корзины пользователя
    pass


class NotEnoughProductQuantityError(BasketError):
    pass
