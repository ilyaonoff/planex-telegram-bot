from aiogram.dispatcher.filters import Text
from aiogram import types
from bot import dp
from bot_logging import logger
from bot import messages
from keyboards import default_keyboard
from states import UserStates


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    logger.info(f'Start or help message from user {message.from_user.id}')
    await UserStates.default.set()
    await message.answer(messages['start'].format(user=message.from_user), reply_markup=default_keyboard)


@dp.message_handler(Text(equals='ℹ️ Информация'),
                    state=[UserStates.default, UserStates.wait_for_task, UserStates.wait_for_answer])
async def info(message: types.Message):
    await message.answer(messages['info'], reply_markup=default_keyboard)
