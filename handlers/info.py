from aiogram import types
from bot import dp
from bot_logging import logger


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    logger.info(f'Start or help message from user {message.from_user.id}')
    await message.answer(f'Hello, {message.from_user.id}')
