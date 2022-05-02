from aiogram import executor, Dispatcher

from bot import dp, event_loop
import handlers, notification, activity_storage


async def on_shutdown(dispatcher: Dispatcher):
    print('Shutdown')
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    notification.notify_scheduler.shutdown()
    activity_storage.activity_storage.shutdown()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=event_loop, on_shutdown=on_shutdown)
