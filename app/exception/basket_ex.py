class BasketError(Exception): # Родительский класс
    pass

class AddProductToBasketError(BasketError): # Ошибка: добавления товара в корзину
    pass

class NotFoundProduct(BasketError): # Ошибка: не найден товар в БД
    pass

class NotEnoughProductQuantityError(BasketError): # Ошибка: недостаточное количество товара в БД
    pass

class NotProductsInBasket(BasketError):
    pass

class RemoveProductFromBasket(BasketError):
    pass