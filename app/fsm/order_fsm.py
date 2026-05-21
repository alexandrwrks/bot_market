from aiogram.fsm.state import State, StatesGroup


class OrderFSM(StatesGroup):
    name = State()
    email = State()
    city = State()
    address = State()
    phone = State()
