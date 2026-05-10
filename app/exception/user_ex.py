class UserError(Exception):
    pass


class NotFoundUserError(UserError):  # Ошибка: не найден пользователь
    pass
