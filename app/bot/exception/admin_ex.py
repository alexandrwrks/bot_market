class AdminError(Exception):
    pass


class AdminInfoError(AdminError):
    pass


class OrdersNotEnough(AdminError):
    pass
