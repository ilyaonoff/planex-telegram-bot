import datetime
from typing import Optional, List, Dict, Any, Tuple

from model.base_training import TwoStageTraining
import utils


class QuestionAnswerTraining(TwoStageTraining):
    intervals = {
        1: datetime.timedelta(days=1),
        2: datetime.timedelta(weeks=1),
        3: datetime.timedelta(weeks=2),
        4: datetime.timedelta(weeks=4)
    }

    def __init__(self, original_collection, user_task_collection, validate_answer):
        super(QuestionAnswerTraining, self).__init__()
        self.original_collection = original_collection
        self.user_task_collection = user_task_collection
        self.validate_answer = validate_answer
        self.active_users = {}

    async def _next_level(self, user_id: int, pred_level=None) -> Optional[int]:
        task_filter = {'user_id': user_id, 'next_training': {'$lte': datetime.datetime.now()}}
        if pred_level is not None:
            task_filter['level'] = {'$lt': pred_level}
        task_with_needed_level = \
            await self.user_task_collection.find(task_filter) \
                .sort('level', -1) \
                .limit(1) \
                .to_list(1)
        if len(task_with_needed_level) == 0:
            return None
        return task_with_needed_level[0]['level']

    async def _random_tasks(self, user_id: int, level: int, time: datetime.datetime) -> List[Dict[str, Any]]:
        return await self.user_task_collection.aggregate([
            {'$match': {'user_id': user_id, 'level': level, 'next_training': {'$lte': time}}},
            {'$project': {'_id': 1, 'task_id': 1}},
            {'$sample': {'size': 5}}
        ]).to_list(5)

    async def get_date_not_empty_training(self, user_id: int) -> datetime.datetime:
        task_filter = {'user_id': user_id}
        task_with_needed_date = \
            await self.user_task_collection.find(task_filter) \
                .sort('next_training', 1) \
                .limit(1) \
                .to_list(1)
        return task_with_needed_date[0]['next_training']

    async def start_training(self, user_id: int) -> Tuple[utils.ViewDict, bool]:
        date_not_empty_training = await self.get_date_not_empty_training(user_id)
        if date_not_empty_training > datetime.datetime.now():
            result = utils.ViewDict({
                'is_started': False,
                'date_not_empty_training': date_not_empty_training
            })
            return result, False
        level = await self._next_level(user_id)
        tasks_to_study = await self._random_tasks(user_id, level, datetime.datetime.now())
        self.active_users[user_id] = {
            'current_level': level,
            'tasks': tasks_to_study,
            'current_task': None,
            'statistics': {
                'total': 0,
                'correct': 0,
                'correct_with_hint': 0
            }
        }
        return utils.ViewDict({'is_started': True}), True

    async def finish_training(self, user_id: int):
        self.active_users.pop(user_id)

    async def first_stage(self, user_id: int) -> Dict:
        user_data = self.active_users[user_id]
        if len(user_data['tasks']) == 0 or user_data['current_task'] == len(user_data['tasks']) - 1:
            level = await self._next_level(user_id, pred_level=user_data['current_level'])
            if level is None:
                return {
                    'is_end': True,
                    'statistics': user_data['statistics']
                }
            tasks_to_study = await self._random_tasks(user_id, level, datetime.datetime.now())
            user_data = self.active_users[user_id] = {
                'current_level': level,
                'tasks': tasks_to_study,
                'current_task': None
            }
        if user_data['current_task'] is None:
            user_data['current_task'] = 0
        else:
            user_data['current_task'] += 1
        task = await self.original_collection.find_one(
            {'_id': user_data['tasks'][user_data['current_task']]['task_id']})
        result = utils.ViewDict({
            'question': task['question'],
            'is_end': False
        })
        return result

    async def _save_task(self, user_data, is_correct):
        if is_correct:
            level = min(4, user_data['current_level'] + 1)
        else:
            level = max(1, user_data['current_level'] - 1)
        next_training = datetime.datetime.now() + QuestionAnswerTraining.intervals[level]
        await self.user_task_collection.update_one(
            {'_id': user_data['tasks'][user_data['current_task']]['_id']},
            {'$set': {'level': level, 'next_training': next_training}},
            upsert=False
        )

    async def second_stage(self, user_id: int, message: str) -> Tuple[Dict, bool]:
        user_data = self.active_users[user_id]
        user_data['statistics']['total'] += 1
        task = await self.original_collection.find_one(
            {'_id': user_data['tasks'][user_data['current_task']]['task_id']})
        is_correct = self.validate_answer(message, task['answer'])
        await self._save_task(user_data, is_correct)
        if is_correct:
            user_data['statistics']['correct'] += 1
        result = utils.ViewDict({
            'is_correct': is_correct,
            'finish_answering': True
        })
        # TODO
        result['association'] = task.get('association',
                                         'CAACAgIAAxkBAAEEx2ViiMaq-ze8gAhdHeKOoVjVhQddOAAC0hAAAqjD4EoueyWr4CsTwyQE')
        return result, True
