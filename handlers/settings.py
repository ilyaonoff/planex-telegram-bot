from aiogram.dispatcher.filters import Text

from bot import dp
from states import UserStates

from aiogram import types
from datetime import datetime
from bot import messages
from keyboards import default_keyboard, settings_keyboard, subject_keyboard, cancel_keyboard
from activity_storage import user
from model import users, subjects


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
    await message.answer(messages['finish_configure'], reply_markup=default_keyboard)


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
    time = await users.set_notification(message.from_user.id, time)
    await UserStates.settings.set()
    await message.answer(messages['new_notification_date'].format(time=time.strftime('%H:%M')),
                         reply_markup=settings_keyboard)


@dp.message_handler(Text(equals='📚 Выбрать предмет'), state=UserStates.settings)
async def set_subject(message: types.Message):
    await UserStates.subject.set()
    await message.answer(messages['start_choosing_subject'], reply_markup=subject_keyboard)


@dp.message_handler(state=UserStates.subject)
async def choose_subject(message: types.Message):
    if message.text not in await subjects.get_available_subjects():
        await message.answer(messages['incorrect_subject_choice'], reply_markup=subject_keyboard)
        return
    with user(message.from_user.id) as can_handle:
        if not can_handle:
            await message.answer(messages['too_frequent_messages'])
            return
        await users.set_subject(message.from_user.id, message.text)
        await UserStates.settings.set()
    await message.answer(messages['finish_choosing_subject'].format(subject=message.text),
                         reply_markup=settings_keyboard)


def parse_interval_message(args: str):
    try:
        return datetime.strptime(args, '%H:%M')
    except ValueError:
        return None
