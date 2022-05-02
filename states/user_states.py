from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    settings = State()
    interval = State()
    subject = State()
    wait_for_task = State()
    wait_for_answer = State()
