from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    choosing_state = State()
    wait_for_task = State()
    wait_for_answer = State()
