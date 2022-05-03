from model.database.client import db_client


async def validate_subject(subject: str) -> bool:
    return subject in ['Обществознание']


async def get_available_subjects():
    return {
        'subjects': ['Обществознание']
    }


def get_task_collection_by_subject_name(subject: str):
    return _task_collection[subject]['task']


def get_user_task_collection_by_subject_name(subject: str):
    return _task_collection[subject]['user_task']


_task_collection = {
    'Обществознание': {
        'task': db_client.planex.society,
        'user_task': db_client.planex.user_society
    }
}
