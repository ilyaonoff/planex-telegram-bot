from aiogram import executor

from bot import dp, event_loop
import handlers, scheduler

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=event_loop)
