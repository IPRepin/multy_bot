from aiogram.fsm.state import StatesGroup, State


class City(StatesGroup):
    NAME = State()


class ChatStates(StatesGroup):
    text = State()
    wait = State()