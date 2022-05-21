from aiogram.dispatcher.filters import Text

import views.task_views
from keyboards import default_keyboard, training_keyboard

from bot import dp, messages
from states import UserStates
from activity_storage import user
from model import training, subjects, users
from views import task_views

from aiogram import types


@dp.message_handler(Text(equals='Тренировка'), state=UserStates.default)
async def start_choose_training(message: types.Message):
    trainings = await subjects.get_available_trainings(await users.get_subject(message.from_user.id))
    await task_views.choose_training(dp, message, trainings)
    await UserStates.choose_training.set()


@dp.message_handler(Text(equals='◀️ Назад'), state=UserStates.choose_training)
async def cancel_choosing_training(message: types.Message):
    await UserStates.default.set()
    await message.answer(messages['back_from_choosing_training'], reply_markup=default_keyboard)


@dp.message_handler(state=UserStates.choose_training)
async def start_training(message: types.Message):
    if message.text not in (await subjects.get_available_trainings(await users.get_subject(message.from_user.id)))['trainings']:
        await message.answer(messages['incorrect_training'])
        return
    model_data, is_started = await training.start_training(message.from_user.id, message.text)
    if is_started:
        await UserStates.wait_for_task.set()
    await views.task_views.start_training(dp, message, model_data)


@dp.message_handler(Text(equals='🔚 Закончить'), state=[UserStates.wait_for_task, UserStates.wait_for_answer])
async def finish_training(message: types.Message):
    await training.finish_training(message.from_user.id)
    await UserStates.default.set()
    await message.answer(messages['interrupt_training'], reply_markup=default_keyboard)


@dp.message_handler(Text(equals='▶ Вперёд'), state=UserStates.wait_for_task)
async def get_task(message: types.Message):
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        task_data = await training.first_stage(message.from_user.id)
        is_end = await task_views.send_task(dp, message, task_data)
        if is_end:
            await training.finish_training(message.from_user.id)
            await UserStates.default.set()
        else:
            await UserStates.wait_for_answer.set()


@dp.message_handler(state=UserStates.wait_for_answer)
async def receive_answer(message: types.Message):
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        answer_data, finish_answering = await training.second_stage(message.from_user.id, message.text)
        await task_views.send_result(dp, message, answer_data)
        if finish_answering:
            await UserStates.wait_for_task.set()
