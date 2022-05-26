from aiogram.dispatcher.filters import Text
from aiogram import types

from bot import dp
from bot_logging import logger
from bot import messages
from keyboards import default_keyboard, settings_keyboard
from states import UserStates
from model import users
import activity_storage
from . import error_handlers


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    logger.info(f'Start message from user {message.from_user.id}')
    with activity_storage.user(message.from_user.id) as can_handle:
        if not can_handle:
            await error_handlers.handle_throttling(message)
            return
        await UserStates.settings.set()
        await message.answer(messages['start'].format(user=message.from_user), reply_markup=settings_keyboard)


@dp.message_handler(Text(equals='ℹ️ Информация'),
                    state=[UserStates.default])
async def info(message: types.Message):
    await message.answer(messages['info'], reply_markup=default_keyboard)


@dp.message_handler()
async def bot_restart_handler(message: types.Message):
    with activity_storage.user(message.from_user.id) as can_handle:
        if not can_handle:
            await error_handlers.handle_throttling(message)
            return
        if await users.is_ready_to_study(message.from_user.id):
            await UserStates.default.set()
            keyboard = default_keyboard
        else:
            await UserStates.settings.set()
            keyboard = settings_keyboard
        await message.answer(messages['bot_was_updated'], reply_markup=keyboard)
