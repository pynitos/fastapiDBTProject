from taskiq import AsyncBroker

from src.diary_ms.infrastructure.tasks.brokers.dispatcher import TaskDispatcher
from src.diary_ms.infrastructure.tasks.diary_cards import create_diary_cards_report


def register_tasks(task_broker: AsyncBroker) -> TaskDispatcher:
    task_1 = task_broker.register_task(create_diary_cards_report)
    task_dispatcher = TaskDispatcher(task_broker)
    task_dispatcher.register_task("create_diary_cards_report", task_1)
    return task_dispatcher
