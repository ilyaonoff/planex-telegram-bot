import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import dp, event_loop, messages, config
from activity_storage import activity_storage


async def _job(user_id: int, min_silence_interval: int):
    last_user_activity = activity_storage.get_last_activity(user_id)
    now = datetime.datetime.now()
    if last_user_activity is None or last_user_activity - now >= datetime.timedelta(hours=min_silence_interval):
        await dp.bot.send_message(user_id, messages['notification'])


class NotificationScheduler:
    def __init__(self, loop, min_silence_interval: int):
        self._scheduler = AsyncIOScheduler(event_loop=loop)
        # TODO configure mongoclient
        self._scheduler.add_jobstore(
            'mongodb',
            database='notification_scheduler'
        )
        self._scheduler.start()
        self.min_silence_interval = min_silence_interval

    def add_notification(self, user_id: int, time: datetime.time):
        self._scheduler.add_job(
            _job, args=(user_id, self.min_silence_interval),
            id=str(user_id), replace_existing=True,
            trigger='cron',
            hour=time.hour.real,
            minute=time.minute.real
        )

    def get_notification_time(self, user_id) -> datetime.time:
        job = self._scheduler.get_job(str(user_id))
        return job.next_run_time.time()

    def remove_notification(self, user_id: int):
        self._scheduler.remove_job(str(user_id))

    def shutdown(self):
        self._scheduler.shutdown()


notify_scheduler = NotificationScheduler(
    event_loop,
    min_silence_interval=config['notification_scheduler']['min_silence_interval_in_hours']
)
