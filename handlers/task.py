from typing import Tuple, Dict

from aiogram.dispatcher import FSMContext
from keyboards import default_keyboard

from bot import dp, messages
from states import UserStates
from activity_storage import user

from aiogram import types
import random

tasks = {
    '123': {'task': 'Answer to any question', 'answer': '42'},
    '5': {'task': 'What is the best telegram bot', 'answer': 'PlanExBot'}
}


def random_task() -> Tuple[str, Dict[str, str]]:
    return random.choice(list(tasks.items()))


@dp.message_handler(state=UserStates.wait_for_task)
async def get_task(message: types.Message, state: FSMContext):
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        task = random_task()
        async with state.proxy() as data:
            data['answer'] = task[1]['answer']
        await UserStates.wait_for_answer.set()
    await message.answer(task[1]['task'], reply_markup=default_keyboard)


@dp.message_handler(state=UserStates.wait_for_answer)
async def receive_answer(message: types.Message, state: FSMContext):
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        async with state.proxy() as data:
            expected_answer = data['answer']
        await UserStates.wait_for_task.set()
    if message.text.lower() == expected_answer:
        await message.answer('Your answer is correct', reply_markup=default_keyboard)
    else:
        await message.answer('You are wrong', reply_markup=default_keyboard)
