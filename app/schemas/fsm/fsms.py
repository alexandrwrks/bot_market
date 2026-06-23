from aiogram.fsm.state import State, StatesGroup


class OrderFSM(StatesGroup):
    name = State()
    phone = State()


class PriceChange(StatesGroup):
    new_price = State()


class QuantityChange(StatesGroup):
    new_quantity = State()


class AddNewProduct(StatesGroup):
    category_id = State()
    name = State()
    description = State()
    price = State()
    quantity = State()
    photo_path = State()


class AddNewCategory(StatesGroup):
    name = State()
    slug = State()
    description = State()
