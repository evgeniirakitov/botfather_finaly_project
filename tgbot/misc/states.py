from aiogram.dispatcher.filters.state import StatesGroup, State


class OurState(StatesGroup):
    Unauthorized = State()


class Purchase(StatesGroup):
    Quantity = State()
    Shipping = State()
    Confirm = State()


class NewItem(StatesGroup):
    Name = State()
    Photo = State()
    Description = State()
    Quantity = State()
    Price = State()
    Confirm = State()
