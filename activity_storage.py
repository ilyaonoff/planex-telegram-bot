from contextlib import contextmanager
from datetime import datetime


class ActivityStorage:
    def __init__(self):
        self._locked = {}
        self._last_activity = {}

    def try_lock(self, user_id: int):
        if self._locked.get(user_id, False):
            return False
        self._locked[user_id] = True
        print(self._last_activity)
        return True

    def try_unlock(self, user_id: int):
        if not self._locked.get(user_id, False):
            return False
        self._locked[user_id] = False
        return True

    def new_activity(self, user_id: int):
        # TODO time zone ???
        self._last_activity[user_id] = datetime.now()

    def get_last_activity(self, user_id: int):
        return self._last_activity.get(user_id, None)


activity_storage = ActivityStorage()


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
