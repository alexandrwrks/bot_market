from aiogram.fsm.state import State, StatesGroup


class OrderFSM(StatesGroup):
    name = State()
    phone = State()

class PriceChange(StatesGroup):
    new_price = State()


class QuantityChange(StatesGroup):
    new_quantity = State()
