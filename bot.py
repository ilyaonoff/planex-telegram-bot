import os
from aiogram import Bot, Dispatcher
import asyncio
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = os.environ['PLANEX_BOT_TOKEN']

event_loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, loop=event_loop, storage=storage)

with open('messages.json') as file:
    messages = json.load(file)