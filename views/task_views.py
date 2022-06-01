from typing import Dict

from aiogram import Dispatcher, types

import utils
from bot import messages
from keyboards import training_keyboard, default_keyboard


async def start_training(dispatcher: Dispatcher, message: types.Message, data: Dict):
    if data['is_started']:
        await message.answer(messages['start_training'], reply_markup=training_keyboard)
    else:
        view_data = utils.ViewDict({
            'date_not_empty_training': data['date_not_empty_training'].strftime("%Y-%m-%d %H:%M")
        })
        await message.answer(messages['nothing_to_train'].format(data=view_data))


async def choose_training(dispatcher: Dispatcher, message: types.Message, data: Dict):
    subject_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in data['trainings']:
        subject_keyboard.add(subject)
    subject_keyboard.add('◀️ Назад')
    await message.answer(messages['choose_training'].format(data=data), reply_markup=subject_keyboard)


async def send_task(dispatcher: Dispatcher, message: types.Message, data: Dict) -> bool:
    if data['is_end']:
        view_data = utils.ViewDict(data['statistics'])
        await message.answer(messages['finish_training'].format(data=view_data), reply_markup=default_keyboard)
        return True
    else:
        await message.answer(data['question'], reply_markup=training_keyboard)
        return False


async def send_result(dispatcher: Dispatcher, message: types.Message, data: Dict):
    if data['is_correct']:
        await message.answer(messages['correct_answer'], reply_markup=training_keyboard)
    else:
        if 'association' in data:
            await message.answer(messages['wrong_answer_with_association'], reply_markup=training_keyboard)
            await message.answer_sticker(data['association'], reply_markup=training_keyboard)
        else:
            await message.answer(messages['wrong_answer'].format(data=data), reply_markup=training_keyboard)
