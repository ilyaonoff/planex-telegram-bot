import datetime
from bot_logging import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import dp, event_loop


async def _job(user_id: str):
    logger.info(f'Run notify job for user {user_id}')
    await dp.bot.send_message(user_id, "It is time to study")


class Scheduler:
    def __init__(self, loop):
        self._scheduler = AsyncIOScheduler(event_loop=loop)
        self._scheduler.start()

    def add_notification(self, user_id: str, time: datetime.datetime):
        self._scheduler.add_job(
            _job, args=(user_id,),
            id=user_id, replace_existing=True,
            trigger='cron',
            hour=time.hour.real,
            minute=time.minute.real
        )

    def remove_notification(self, user_id: str):
        self._scheduler.remove_job(user_id)

    def shutdown(self):
        self._scheduler.shutdown()


scheduler = Scheduler(event_loop)
