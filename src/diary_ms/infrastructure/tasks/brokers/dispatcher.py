from collections.abc import Callable
from typing import Any

from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask, AsyncTaskiqTask

from src.diary_ms.application.common.exceptions.base import InfraError
from src.diary_ms.application.common.interfaces.task_sender import TaskSender


class TaskDispatcher(TaskSender):
    def __init__(self, broker: AsyncBroker) -> None:
        self._broker = broker
        self.tasks: dict[str, Callable] = {}

    def register_task(self, task_name: str, task: Callable) -> None:
        self.tasks[task_name] = task

    async def send_task(self, task_name: str) -> str:
        task_func: Callable | None = self.tasks.get(task_name)
        if not task_func:
            raise InfraError
        task_: AsyncTaskiqDecoratedTask = self._broker.task(task_func)
        task: AsyncTaskiqTask = await task_.kiq()
        await task.wait_result()
        return task.task_id

    async def get_result(self, task_id: str) -> Any:
        result = await self._broker.result_backend.get_result(task_id)
        return result.return_value
