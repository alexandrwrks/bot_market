from aiogram.fsm.state import State, StatesGroup


class OrderFSM(StatesGroup):
    name = State()
    phone = State()
