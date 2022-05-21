import datetime
from typing import Dict, Optional, Tuple

from model.database.client import db_client
from notification import notify_scheduler
from .training import init_subject, is_first_time
import utils


async def get_subject(user_id: int) -> Optional[str]:
    user = await db_client.planex.users.find_one({'user_id': user_id})
    if 'subject' in user:
        return user['subject']
    else:
        return None


async def set_subject(user_id: int, subject: str) -> Dict:
    users_collection = db_client.planex.users
    await users_collection.update_one({'user_id': user_id}, {'$set': {'subject': subject}}, upsert=True)
    if await is_first_time(user_id, subject):
        await init_subject(user_id, subject)
    result = utils.ViewDict({
        'new_subject': subject
    })
    return result


async def set_training(user_id: int, training: str):
    users_collection = db_client.planex.users
    await users_collection.update_one({'user_id': user_id}, {'$set': {'training': training}})


async def get_training(user_id: int) -> Optional[Tuple[str, str]]:
    user = await db_client.planex.users.find_one({'user_id': user_id})
    if 'training' in user:
        return user['subject'], user['training']
    else:
        return None


async def is_ready_to_study(user_id: int) -> bool:
    users_collection = db_client.planex.users
    return await users_collection.find_one({'user_id': user_id, 'subject': {'$exists': True}}) is not None


async def get_notification_time(user_id: int) -> datetime.time:
    return notify_scheduler.get_notification_time(user_id)


async def set_notification_time(user_id: int, time: datetime.time) -> Dict:
    notify_scheduler.add_notification(user_id, time)
    result = utils.ViewDict({
        'new_notification_time': time
    })
    return result
