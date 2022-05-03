import datetime
from typing import Dict

from . import users
from .question_answer_training import QuestionAnswerTraining
from .base_training import TwoStageTraining
from . import subjects


async def init_subject(user_id: int, subject: str):
    task_collection = subjects.get_task_collection_by_subject_name(subject)
    user_task_collection = subjects.get_user_task_collection_by_subject_name(subject)
    async for task in task_collection.find():
        user_task = {
            'task_id': task['_id'],
            'user_id': user_id,
            'level': 1,
            'next_training': datetime.datetime.now()
        }
        await user_task_collection.insert_one(user_task)


async def is_first_time(user_id: int, subject: str) -> bool:
    user_task_collection = subjects.get_user_task_collection_by_subject_name(subject)
    user_task = await user_task_collection.find_one({'user_id': user_id})
    return user_task is None


async def start_training(user_id: int):
    user_subject = await users.get_subject(user_id)
    await trainings[user_subject].start_training(user_id)


async def finish_training(user_id: int):
    user_subject = await users.get_subject(user_id)
    await trainings[user_subject].finish_training(user_id)


async def first_stage(user_id: int) -> Dict:
    user_subject = await users.get_subject(user_id)
    return await trainings[user_subject].first_stage(user_id)


async def second_stage(user_id: int, message: str) -> Dict:
    user_subject = await users.get_subject(user_id)
    return await trainings[user_subject].second_stage(user_id, message)


trainings: Dict[str, TwoStageTraining] = {
    'Обществознание': QuestionAnswerTraining(
        original_collection=subjects.get_task_collection_by_subject_name('Обществознание'),
        user_task_collection=subjects.get_user_task_collection_by_subject_name('Обществознание')
    )
}
