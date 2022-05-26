import abc
from typing import Dict


class TwoStageTraining(abc.ABC):
    @abc.abstractmethod
    async def start_training(self, user_id: int):
        pass

    @abc.abstractmethod
    async def finish_training(self, user_id: int):
        pass

    @abc.abstractmethod
    async def first_stage(self, user_id: int) -> Dict:
        pass

    @abc.abstractmethod
    async def second_stage(self, user_id: int, message: str) -> Dict:
        pass
