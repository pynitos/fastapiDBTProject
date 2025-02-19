from typing import Any

from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask, AsyncTaskiqTask

from src.diary_ms.application.common.exceptions.base import InfraError
from src.diary_ms.application.common.interfaces.task_sender import TaskSender


class TaskDispatcher(TaskSender):
    def __init__(self, broker: AsyncBroker) -> None:
        self._broker = broker
        self.tasks: dict[str, AsyncTaskiqDecoratedTask] = {}

    def register_task(self, task_name: str, task: AsyncTaskiqDecoratedTask) -> None:
        self.tasks[task_name] = task

    async def send_task(self, task_name: str) -> str:
        task_: AsyncTaskiqDecoratedTask | None = self.tasks.get(task_name)
        if not task_:
            raise InfraError
        task: AsyncTaskiqTask = await task_.kiq()
        return task.task_id

    async def get_result(self, task_id: str) -> Any:
        result = await self._broker.result_backend.get_result(task_id)
        return result.return_value
