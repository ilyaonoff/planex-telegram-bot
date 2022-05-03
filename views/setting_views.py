from typing import Dict

from aiogram import Dispatcher, types

from bot import messages
from keyboards import settings_keyboard


async def available_subjects(dispatcher: Dispatcher, message: types.Message, data: Dict):
    subject_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in data['subjects']:
        subject_keyboard.add(subject)
    await message.answer(messages['start_choosing_subject'], reply_markup=subject_keyboard)


async def notification_setup(dispatcher: Dispatcher, message: types.Message, data: Dict):
    await message.answer(messages['new_notification_date'], reply_markup=settings_keyboard)


async def subject_setup(dispatcher: Dispatcher, message: types.Message, data: Dict):
    await message.answer(messages['finish_choosing_subject'], reply_markup=settings_keyboard)
