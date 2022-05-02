import os
from aiogram import Bot, Dispatcher
import asyncio
import json
from aiogram.contrib.fsm_storage.mongo import MongoStorage

TOKEN = os.environ['PLANEX_BOT_TOKEN']

event_loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN)
# TODO configure mongoclient
storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')
dp = Dispatcher(bot, loop=event_loop, storage=storage)

with open('messages.json') as file:
    messages = json.load(file)

with open('config.json') as file:
    config = json.load(file)
