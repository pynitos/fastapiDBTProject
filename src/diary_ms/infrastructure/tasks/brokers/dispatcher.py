from datetime import datetime
from typing import Any

from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask, AsyncTaskiqTask, ScheduleSource
from taskiq.scheduler.created_schedule import CreatedSchedule

from diary_ms.application.common.exceptions.base import InfraError
from diary_ms.application.common.interfaces.task_sender import TaskSender


class TaskDispatcher(TaskSender):
    def __init__(self, broker: AsyncBroker, schedule_sourse: ScheduleSource) -> None:
        self._broker = broker
        self._schedule_sourse = schedule_sourse

    async def send_task(
        self, task_name: str, schedule_time: str | datetime | None = None, *args: Any, **kwargs: Any
    ) -> str:
        decorated_task: AsyncTaskiqDecoratedTask[Any, Any] | None = self._broker.find_task(task_name)
        if not decorated_task:
            raise InfraError
        schedule: CreatedSchedule[Any]
        if isinstance(schedule_time, str):
            schedule = await decorated_task.schedule_by_cron(self._schedule_sourse, schedule_time, *args, **kwargs)
            return schedule.schedule_id
        elif isinstance(schedule_time, datetime):
            schedule = await decorated_task.schedule_by_time(self._schedule_sourse, schedule_time, *args, **kwargs)
            return schedule.schedule_id
        task: AsyncTaskiqTask[Any] = await decorated_task.kiq(*args, **kwargs)
        return task.task_id

    async def get_result(self, task_id: str) -> Any:
        result = await self._broker.result_backend.get_result(task_id)
        return result.return_value
