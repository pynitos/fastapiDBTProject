from abc import abstractmethod
from typing import Any, Protocol


class TaskSender(Protocol):
    @abstractmethod
    async def send_task(self, task_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_result(self, task_id: str) -> Any:
        raise NotImplementedError
