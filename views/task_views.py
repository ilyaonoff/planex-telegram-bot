from typing import Dict

from aiogram import Dispatcher, types

from keyboards import training_keyboard, default_keyboard


async def send_task(dispatcher: Dispatcher, message: types.Message, data: Dict) -> bool:
    if data['is_end']:
        await message.answer('This training has been finished', reply_markup=default_keyboard)
        return True
    else:
        await message.answer(data['task'], reply_markup=training_keyboard)
        return False


async def send_result(dispatcher: Dispatcher, message: types.Message, data: Dict):
    if data['is_correct']:
        await message.answer('You are right)', reply_markup=training_keyboard)
    else:
        await message.answer('You are wrong(', reply_markup=training_keyboard)
