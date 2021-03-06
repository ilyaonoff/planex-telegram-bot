import os, time
from aiogram import Bot, Dispatcher
import asyncio
import json

from aiogram.contrib.fsm_storage.memory import MemoryStorage

os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

TOKEN = os.getenv('BOT_TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

MONGODB_URI = os.getenv('MONGODB_URI')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with open('messages.json') as file:
    messages = json.load(file)

with open('config.json') as file:
    config = json.load(file)
