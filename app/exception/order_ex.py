class OrderError(Exception):
    pass


class PlaceOrderError(OrderError):
    pass


class NotUserOrder(OrderError):
    # Не найдены заказы пользователя
    pass


class CostEnoughError(OrderError):
    pass

class CreateOrderError(OrderError):
    pass