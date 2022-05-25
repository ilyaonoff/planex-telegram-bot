from typing import Dict

from aiogram import Dispatcher, types

from bot import messages
from keyboards import settings_keyboard
import utils


async def available_subjects(dispatcher: Dispatcher, message: types.Message, data: Dict):
    subject_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in data['subjects']:
        subject_keyboard.add(subject)
    await message.answer(messages['start_choosing_subject'], reply_markup=subject_keyboard)


async def notification_setup(dispatcher: Dispatcher, message: types.Message, data: Dict):
    view_data = utils.ViewDict({'new_notification_time': data['new_notification_time'].strftime("%H:%M")})
    await message.answer(messages['new_notification_date'].format(data=view_data), reply_markup=settings_keyboard)


async def subject_setup(dispatcher: Dispatcher, message: types.Message, data: Dict):
    response = messages['finish_choosing_subject'].format(data=data)
    if data['is_ready_to_study']:
        response += '\n\n' + messages['info_about_settings']
    await message.answer(response, reply_markup=settings_keyboard)
