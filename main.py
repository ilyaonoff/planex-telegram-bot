from aiogram import executor, Dispatcher

import bot
import handlers, notification, activity_storage
from notification import notify_scheduler
from activity_storage import activity_storage


async def on_shutdown(dispatcher: Dispatcher):
    print('Shutdown')
    await bot.bot.delete_webhook()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    notification.notify_scheduler.shutdown()
    activity_storage.shutdown()


async def on_startup(dispatcher: Dispatcher):
    await bot.bot.set_webhook(bot.WEBHOOK_URL, drop_pending_updates=True)
    notify_scheduler.start()
    activity_storage.start()


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=bot.dp,
        webhook_path=bot.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=bot.WEBAPP_HOST,
        port=bot.WEBAPP_PORT,
    )
