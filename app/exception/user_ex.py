class UserError(Exception):
    pass


class NotFoundUserError(UserError):  # Ошибка: не найден пользователь
    pass


class UserAdminLicense(UserError):  # Отсутствие админки у пользователя
    pass
