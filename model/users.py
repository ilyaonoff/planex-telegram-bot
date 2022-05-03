import datetime
from typing import Dict

from model.database.client import db_client
from notification import notify_scheduler
from .tasks import init_subject, is_first_time


async def set_subject(user_id: int, subject: str) -> Dict:
    users_collection = db_client.planex.users
    await users_collection.update_one({'user_id': user_id}, {'$set': {'subject': subject}}, upsert=True)
    if await is_first_time(user_id, subject):
        await init_subject(user_id, subject)
    result = {
        'new_subject': subject
    }
    return result


async def is_ready_to_study(user_id: int):
    users_collection = db_client.planex.users
    return await users_collection.count_documents({'user_id': user_id, 'subject': {'$exists': True}}) > 0


async def set_notification(user_id: int, time: datetime.datetime) -> Dict:
    notify_scheduler.add_notification(user_id, time)
    result = {
        'new_notification_time': time
    }
    return result
