from aiogram import types

from bot import messages


async def handle_throttling(message: types.Message):
    await message.answer(messages['too_frequent_messages'])
