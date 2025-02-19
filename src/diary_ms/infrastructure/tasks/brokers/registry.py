from taskiq import AsyncBroker

from src.diary_ms.infrastructure.tasks.diary_cards import create_diary_cards_report


def register_tasks(task_broker: AsyncBroker):
    task_broker.register_task(create_diary_cards_report)
    return task_broker
