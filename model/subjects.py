from typing import Dict

from model.database.client import db_client
import utils


async def validate_subject(subject: str) -> bool:
    return subject in ['Обществознание']


async def get_available_trainings(subject: str) -> Dict:
    return utils.ViewDict({
        'subject': subject,
        'trainings': ['Термины']
    })


async def get_available_subjects():
    return utils.ViewDict({
        'subjects': ['Обществознание']
    })


def get_task_collection_by_subject_name(subject: str, training: str):
    return _task_collection[subject][training]['task']


def get_user_task_collection_by_subject_name(subject: str, training: str):
    return _task_collection[subject][training]['user_task']


_task_collection = {
    'Обществознание': {
        'Термины': {
            'task': db_client.planex.society.terms,
            'user_task': db_client.planex.user_society.terms
        }
    }
}
