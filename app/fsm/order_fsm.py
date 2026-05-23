from aiogram.fsm.state import State, StatesGroup


class OrderFSM(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    email = State()
    city = State()
    address = State()
