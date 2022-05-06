import datetime
from typing import Dict

from . import users
from .question_answer_training import QuestionAnswerTraining
from .base_training import TwoStageTraining
from . import subjects


async def init_subject(user_id: int, subject: str):
    subject_trainings = await subjects.get_available_trainings(subject)
    for training in subject_trainings['trainings']:
        task_collection = subjects.get_task_collection_by_subject_name(subject, training)
        user_task_collection = subjects.get_user_task_collection_by_subject_name(subject, training)
        async for task in task_collection.find():
            user_task = {
                'task_id': task['_id'],
                'user_id': user_id,
                'level': 1,
                'next_training': datetime.datetime.now()
            }
            await user_task_collection.insert_one(user_task)


async def is_first_time(user_id: int, subject: str) -> bool:
    subject_trainings = await subjects.get_available_trainings(subject)
    user_task_collection = subjects.get_user_task_collection_by_subject_name(subject, subject_trainings['trainings'][0])
    user_task = await user_task_collection.find_one({'user_id': user_id})
    return user_task is None


async def start_training(user_id: int, training: str):
    user_subject = await users.get_subject(user_id)
    await users.set_training(user_id, training)
    await trainings[user_subject][training].start_training(user_id)


async def finish_training(user_id: int):
    user_subject, user_training = await users.get_training(user_id)
    await trainings[user_subject][user_training].finish_training(user_id)


async def first_stage(user_id: int) -> Dict:
    user_subject, user_training = await users.get_training(user_id)
    return await trainings[user_subject][user_training].first_stage(user_id)


async def second_stage(user_id: int, message: str) -> Dict:
    user_subject, user_training = await users.get_training(user_id)
    return await trainings[user_subject][user_training].second_stage(user_id, message)


trainings: Dict[str, Dict[str, TwoStageTraining]] = {
    'Обществознание': {
        'Термины': QuestionAnswerTraining(
            original_collection=subjects.get_task_collection_by_subject_name('Обществознание', 'Термины'),
            user_task_collection=subjects.get_user_task_collection_by_subject_name('Обществознание', 'Термины')
        )
    }
}
