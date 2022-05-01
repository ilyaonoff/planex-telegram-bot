from bot import dp
from scheduler.scheduler import scheduler
from states import UserStates

from aiogram import types
from datetime import datetime
from bot import messages


@dp.message_handler(commands='interval', state='*')
async def set_interval(message: types.Message):
    args = message.get_args()
    if not args.strip():
        return await message.answer(messages['current_notify_info'].format(time=datetime.now().strftime('%H:%M')))  # TODO
    time = parse_interval_message(args)
    if time is None:
        return await message.answer(messages['incorrect_interval_query'])
    scheduler.add_notification(str(message.from_user.id), time)
    return await message.answer(messages['new_notify_info'].format(time=time.strftime('%H:%M')))


@dp.message_handler(commands='subject', state='*')
async def set_subject(message: types.Message):
    await UserStates.choosing_state.set()
    keyboard = create_subject_keyboard()
    await message.answer(messages['choosing_subject'], reply_markup=keyboard)


@dp.message_handler(state=UserStates.choosing_state)
async def choose_subject(message: types.Message):
    if message.text not in available_subjects:
        keyboard = create_subject_keyboard()
        return await message.answer(messages['incorrect_subject_choice'], reply_markup=keyboard)
    await UserStates.wait_for_task.set()
    await message.answer(messages['chosen_subject'].format(subject=message.text))


def parse_interval_message(args: str):
    try:
        return datetime.strptime(args, '%H:%M')
    except ValueError:
        return None


available_subjects = ['English language', 'Math', 'Russian language']


def create_subject_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = available_subjects
    keyboard.add(*buttons)
    return keyboard
