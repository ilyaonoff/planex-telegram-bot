import datetime
from typing import Dict, Optional, List, Any


from model.database.client import db_client


active_users = {}
intervals = {
    1: datetime.timedelta(days=1),
    2: datetime.timedelta(weeks=1),
    3: datetime.timedelta(weeks=2),
    4: datetime.timedelta(weeks=4)
}


async def init_subject(user_id: int, subject: str):
    original_tasks = db_client.planex.original_tasks.find()
    async for task in original_tasks:
        user_task = {
            'task_id': task['_id'],
            'user_id': user_id,
            'level': 1,
            'next_training': datetime.datetime.now()
        }
        await db_client.planex.tasks.insert_one(user_task)


async def is_first_time(user_id: int, subject: str) -> bool:
    user_task = await db_client.planex.tasks.find_one({'user_id': user_id})
    return user_task is None


async def next_level(user_id: int, subject: str, pred_level=None) -> Optional[int]:
    task_filter = {'user_id': user_id, 'next_training': {'$lte': datetime.datetime.now()}}
    if pred_level is not None:
        task_filter['level'] = {'$lt': pred_level}
    task_with_needed_level = \
        await db_client.planex.tasks.find(task_filter)\
        .sort('level', -1)\
        .limit(1)\
        .to_list(1)
    if len(task_with_needed_level) == 0:
        return None
    return task_with_needed_level[0]['level']


async def random_tasks(user_id: int, subject: str, level: int, time: datetime.datetime) -> List[Dict[str, Any]]:
    return await db_client.planex.tasks.aggregate([
        {'$match': {'user_id': user_id, 'level': level, 'next_training': {'$lte': time}}},
        {'$project': {'_id': 1, 'task_id': 1}},
        {'$sample': {'size': 5}}
    ]).to_list(5)


async def start_training(user_id: int):
    level = await next_level(user_id, 'subject')
    tasks_to_study = await random_tasks(user_id, 'subject', level, datetime.datetime.now())
    active_users[user_id] = {
        'current_level': level,
        'tasks': tasks_to_study,
        'current_task': None
    }


async def finish_training(user_id: int):
    active_users.pop(user_id)


async def get_task(user_id: int) -> Dict:
    user_data = active_users[user_id]
    if len(user_data['tasks']) == 0 or user_data['current_task'] == len(user_data['tasks']) - 1:
        level = await next_level(user_id, 'subject', pred_level=user_data['current_level'])
        if level is None:
            return {'is_end': True}
        tasks_to_study = await random_tasks(user_id, 'subject', level, datetime.datetime.now())
        user_data = active_users[user_id] = {
            'current_level': level,
            'tasks': tasks_to_study,
            'current_task': None
        }
    if user_data['current_task'] is None:
        user_data['current_task'] = 0
    else:
        user_data['current_task'] += 1
    task = await db_client.planex.original_tasks.find_one({'_id': user_data['tasks'][user_data['current_task']]['task_id']})
    result = {
        'task': task['task'],
        'is_end': False
    }
    return result


async def receive_answer(user_id: int, answer: str) -> Dict:
    user_data = active_users[user_id]
    task = await db_client.planex.original_tasks.find_one({'_id': user_data['tasks'][user_data['current_task']]['task_id']})
    is_correct = task['answer'].strip() == answer
    if is_correct:
        level = min(4, user_data['current_level'] + 1)
    else:
        level = max(1, user_data['current_level'] - 1)
    next_training = datetime.datetime.now() + intervals[level]
    await db_client.planex.tasks.update_one(
        {'_id': user_data['tasks'][user_data['current_task']]['_id']},
        {'$set': {'level': level, 'next_training': next_training}},
        upsert=False
    )
    result = {
        'is_correct': is_correct
    }
    return result
