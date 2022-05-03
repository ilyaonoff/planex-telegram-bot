import random
from typing import Tuple, Dict
from model.database.client import db_client

tasks = {
    '123': {'task': 'Answer to any question', 'answer': '42'},
    '5': {'task': 'What is the best telegram bot', 'answer': 'PlanExBot'}
}


def random_task() -> Tuple[str, Dict[str, str]]:
    return random.choice(list(tasks.items()))


async def start_training(user_id: int):
    pass


async def finish_training(user_id: int):
    pass


async def get_task(user_id: int) -> str:
    task = random_task()
    users_collection = db_client.planex.users
    await users_collection.update_one({'user_id': user_id}, {'$set': {'task_id': task[0]}})
    return task[1]['task']


async def receive_answer(user_id: int, answer: str) -> bool:
    users_collection = db_client.planex.users
    user = await users_collection.find_one({'user_id': user_id})
    task_id = user['task_id']
    # TODO maybe you should delete field task_id
    return tasks[task_id]['answer'].strip() == answer
