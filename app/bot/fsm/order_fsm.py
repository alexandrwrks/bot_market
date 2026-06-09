from aiogram.fsm.state import State, StatesGroup
from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    address: str | None
    full_name: str | None
    phone: str | None


class NewAddress(StatesGroup):
    address = State()

class NewFullName(StatesGroup):
    full_name = State()

class NewPhone(StatesGroup):
    phone = State()