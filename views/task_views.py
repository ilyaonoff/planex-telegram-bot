from typing import Dict

from aiogram import Dispatcher, types

from bot import messages
from keyboards import training_keyboard, default_keyboard


async def choose_training(dispatcher: Dispatcher, message: types.Message, data: Dict):
    subject_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in data['trainings']:
        subject_keyboard.add(subject)
    await message.answer(messages['choose_training'], reply_markup=subject_keyboard)


async def send_task(dispatcher: Dispatcher, message: types.Message, data: Dict) -> bool:
    if data['is_end']:
        await message.answer('This training has been finished', reply_markup=default_keyboard)
        return True
    else:
        await message.answer(data['question'], reply_markup=training_keyboard)
        return False


async def send_result(dispatcher: Dispatcher, message: types.Message, data: Dict):
    if data['is_correct']:
        await message.answer('Ты молодец! Нажимай "вперед", и идем дальше :)', reply_markup=training_keyboard)
    else:
        await message.answer('You are wrong(', reply_markup=training_keyboard)
