from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import event_loop, config
from bot_logging import logger


class ActivityStorage:
    def __init__(self, loop, first_clean_date: datetime, clean_interval: int, silence_interval):
        self._locked = {}
        self._last_activity = {}
        self.silence_interval = silence_interval
        self._scheduler = AsyncIOScheduler(event_loop=loop)
        self._scheduler.add_job(
            self._clean,
            'interval',
            start_date=first_clean_date,
            days=clean_interval
        )
        self._scheduler.start()

    def _clean(self):
        logger.info(f'The number of active users before cleaning: {len(self._last_activity)}')
        now = datetime.now()
        for user_id in self._last_activity.keys():
            last_activity = self._last_activity[user_id]
            if not self._locked[user_id] and last_activity - now >= timedelta(days=self.silence_interval):
                self._locked.pop(user_id)
                self._last_activity.pop(user_id)
        logger.info(f'The number of active users after cleaning: {len(self._last_activity)}')

    def try_lock(self, user_id: int) -> bool:
        if self._locked.get(user_id, False):
            return False
        self._locked[user_id] = True
        return True

    def try_unlock(self, user_id: int) -> bool:
        if not self._locked.get(user_id, False):
            return False
        self._locked[user_id] = False
        return True

    def new_activity(self, user_id: int):
        # TODO time zone ???
        self._last_activity[user_id] = datetime.now()

    def get_last_activity(self, user_id: int) -> Optional[datetime]:
        return self._last_activity.get(user_id, None)

    def shutdown(self):
        self._scheduler.shutdown()


activity_storage = ActivityStorage(
    event_loop,
    first_clean_date=config['activity_storage']['first_clean_date'],
    clean_interval=config['activity_storage']['clean_interval_in_days'],
    silence_interval=config['activity_storage']['silence_interval_in_days']
)


@contextmanager
def user(user_id: int):
    locked = False
    try:
        locked = activity_storage.try_lock(user_id)
        if locked:
            activity_storage.new_activity(user_id)
        yield locked
    finally:
        if locked:
            activity_storage.try_unlock(user_id)
