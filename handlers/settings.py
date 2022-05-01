from aiogram.dispatcher.filters import Text

from bot import dp
from scheduler.scheduler import scheduler
from states import UserStates

from aiogram import types
from datetime import datetime
from bot import messages
from keyboards import default_keyboard, settings_keyboard, subject_keyboard, cancel_keyboard


@dp.message_handler(Text(equals='⚙️ Настроить'), state='*')
async def configure(message: types.Message):
    await UserStates.settings.set()
    await message.answer('You can configure interval or subject', reply_markup=settings_keyboard)


@dp.message_handler(Text(equals='◀️ Назад'), state=UserStates.settings)
async def back_from_configure(message: types.Message):
    # TODO check that user is ready to study
    await UserStates.wait_for_task.set()
    await message.answer('You are ready to study', reply_markup=default_keyboard)


@dp.message_handler(Text(equals='🕘 Выбрать интервал'), state=UserStates.settings)
async def configure_interval(message: types.Message):
    await UserStates.interval.set()
    await message.answer('Please send me time with format HH:MM', reply_markup=cancel_keyboard)


@dp.message_handler(Text(equals='◀️ Отменить'), state=UserStates.interval)
async def cancel_choosing_interval(message: types.Message):
    await UserStates.settings.set()
    await message.answer('Interval was not changed', reply_markup=settings_keyboard)


@dp.message_handler(state=UserStates.interval)
async def set_interval(message: types.Message):
    args = message.text
    time = parse_interval_message(args)
    if time is None:
        return await message.answer(messages['incorrect_interval_query'])
    await UserStates.settings.set()
    scheduler.add_notification(str(message.from_user.id), time)
    await message.answer(messages['new_notify_info'].format(time=time.strftime('%H:%M')),
                         reply_markup=settings_keyboard)


@dp.message_handler(Text(equals='📚 Выбрать предмет'), state=UserStates.settings)
async def set_subject(message: types.Message):
    await UserStates.subject.set()
    await message.answer(messages['choosing_subject'], reply_markup=subject_keyboard)


@dp.message_handler(state=UserStates.subject)
async def choose_subject(message: types.Message):
    if message.text not in available_subjects:
        return await message.answer(messages['incorrect_subject_choice'], reply_markup=subject_keyboard)
    await UserStates.settings.set()
    await message.answer(messages['chosen_subject'].format(subject=message.text), reply_markup=settings_keyboard)


def parse_interval_message(args: str):
    try:
        return datetime.strptime(args, '%H:%M')
    except ValueError:
        return None


available_subjects = ['English language', 'Math', 'Russian language']

