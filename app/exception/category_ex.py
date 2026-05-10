class CategoryError(Exception):
    pass


class NotCategoryError(CategoryError):
    """Отсутствие категорий"""

    pass
