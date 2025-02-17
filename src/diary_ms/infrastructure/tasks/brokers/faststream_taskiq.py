from typing import Any

from taskiq_faststream import BrokerWrapper

from src.diary_ms.application.common.interfaces.task_sender import TaskSender


class FaststreamTaskiqTaskSenderImpl(TaskSender):
    def __init__(self, task_broker: BrokerWrapper):
        self._task_broker = task_broker

    async def send_task(self, message: Any, topic: str, schedule: list[Any]) -> str:
        task = self._task_broker.task(
            message=message,
            topic=topic,
            schedule=schedule,
        )
        task = await task.kiq()
        return task.task_id

    async def get_result(self, task_id: str) -> Any:
        result = await self._task_broker.result_backend.get_result(task_id)
        return result.return_value
