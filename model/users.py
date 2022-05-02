import datetime

from model.database.client import db_client
from scheduler import scheduler


async def set_subject(user_id: int, subject: str):
    users_collection = db_client.planex.users
    await users_collection.update_one({'user_id': user_id}, {'$set': {'subject': subject}}, upsert=True)


async def is_ready_to_study(user_id: int):
    users_collection = db_client.planex.users
    return await users_collection.count_documents({'user_id': user_id, 'subject': {'$exists': True}}) > 0


async def set_notification(user_id: int, time: datetime.datetime):
    scheduler.add_notification(user_id, time)
    return time
