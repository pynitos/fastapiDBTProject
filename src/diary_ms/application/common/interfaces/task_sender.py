from abc import abstractmethod
from datetime import datetime
from typing import Any, Protocol


class TaskSender(Protocol):
    @abstractmethod
    async def send_task(
        self, task_name: str, schedule_time: str | datetime | None = None, *args: Any, **kwargs: Any
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_result(self, task_id: str) -> Any:
        raise NotImplementedError
