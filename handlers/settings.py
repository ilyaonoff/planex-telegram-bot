from typing import Optional

from aiogram.dispatcher.filters import Text

import utils
from bot import dp
from states import UserStates

from aiogram import types
import datetime
from bot import messages
from keyboards import default_keyboard, settings_keyboard, cancel_keyboard
from activity_storage import user
from model import users, subjects
from views import setting_views


@dp.message_handler(Text(equals='⚙️ Настроить'), state='*')
async def configure(message: types.Message):
    await UserStates.settings.set()
    await message.answer(messages['start_configure'], reply_markup=settings_keyboard)


@dp.message_handler(Text(equals='◀️ Назад'), state=UserStates.settings)
async def back_from_configure(message: types.Message):
    if not await users.is_ready_to_study(message.from_user.id):
        await message.answer(messages['unfinished_configuration'], reply_markup=settings_keyboard)
        return
    await UserStates.default.set()
    training_time = await users.get_notification_time(message.from_user.id)
    subject = await users.get_subject(message.from_user.id)
    data = utils.ViewDict({'training_time': training_time.strftime("%H:%M"), 'subject': subject})
    await message.answer(messages['finish_configure'].format(data=data), reply_markup=default_keyboard)


@dp.message_handler(Text(equals='🕘 Выбрать интервал'), state=UserStates.settings)
async def configure_interval(message: types.Message):
    await UserStates.interval.set()
    await message.answer(messages['choose_notification_date'], reply_markup=cancel_keyboard)


@dp.message_handler(Text(equals='◀️ Отменить'), state=UserStates.interval)
async def cancel_choosing_interval(message: types.Message):
    await UserStates.settings.set()
    await message.answer(messages['back_from_notification_configuration'], reply_markup=settings_keyboard)


@dp.message_handler(state=UserStates.interval)
async def set_interval(message: types.Message):
    args = message.text
    time = parse_interval_message(args)
    if time is None:
        await message.answer(messages['incorrect_notification_date'])
        return
    notification_data = await users.set_notification_time(message.from_user.id, time)
    await setting_views.notification_setup(dp, message, notification_data)
    await UserStates.settings.set()


@dp.message_handler(Text(equals='📚 Выбрать предмет'), state=UserStates.settings)
async def set_subject(message: types.Message):
    await UserStates.subject.set()
    subject_data = await subjects.get_available_subjects()
    await setting_views.available_subjects(dp, message, subject_data)


@dp.message_handler(state=UserStates.subject)
async def choose_subject(message: types.Message):
    if not await subjects.validate_subject(message.text):
        await message.answer(messages['incorrect_subject_choice'])
        return
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        subject_data = await users.set_subject(message.from_user.id, message.text)
        await setting_views.subject_setup(dp, message, subject_data)
        await UserStates.settings.set()


def parse_interval_message(args: str) -> Optional[datetime.time]:
    try:
        return datetime.datetime.strptime(args, '%H:%M').time()
    except ValueError:
        return None
