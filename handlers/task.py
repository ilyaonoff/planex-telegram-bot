from aiogram.dispatcher.filters import Text

from keyboards import default_keyboard, training_keyboard

from bot import dp, messages
from states import UserStates
from activity_storage import user
from model import tasks

from aiogram import types


@dp.message_handler(Text(equals='Тренировка'), state=UserStates.default)
async def start_training(message: types.Message):
    await tasks.start_training(message.from_user.id)
    await UserStates.wait_for_task.set()
    await message.answer(messages['start_training'], reply_markup=training_keyboard)


@dp.message_handler(Text(equals='🔚 Закончить'), state=[UserStates.wait_for_task, UserStates.wait_for_answer])
async def finish_training(message: types.Message):
    await tasks.finish_training(message.from_user.id)
    await UserStates.default.set()
    await message.answer(messages['finish_training'], reply_markup=default_keyboard)


@dp.message_handler(state=UserStates.wait_for_task)
async def get_task(message: types.Message):
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        task_text = await tasks.get_task(message.from_user.id)
        await UserStates.wait_for_answer.set()
    await message.answer(task_text, reply_markup=training_keyboard)


@dp.message_handler(state=UserStates.wait_for_answer)
async def receive_answer(message: types.Message):
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        result = await tasks.receive_answer(message.from_user.id, message.text)
        await UserStates.wait_for_task.set()
    if result:
        await message.answer('Your answer is correct', reply_markup=training_keyboard)
    else:
        await message.answer('You are wrong', reply_markup=training_keyboard)
