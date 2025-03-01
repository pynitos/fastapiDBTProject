from taskiq import AsyncBroker

from src.diary_ms.infrastructure.tasks.brokers.dispatcher import TaskDispatcher
from src.diary_ms.infrastructure.tasks.diary_cards import create_diary_cards_report


def register_tasks(task_broker: AsyncBroker) -> None:
    task_broker.register_task(create_diary_cards_report, "create_diary_cards_report")


def get_task_dispatcher(task_broker: AsyncBroker) -> TaskDispatcher:
    task_dispatcher = TaskDispatcher(task_broker)
    task_dispatcher.register_task("create_diary_cards_report", create_diary_cards_report)
    return task_dispatcher
