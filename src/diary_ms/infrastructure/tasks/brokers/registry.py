from taskiq import AsyncBroker

from diary_ms.infrastructure.tasks.tasks.diary_cards import create_diary_cards_report


def register_tasks(task_broker: AsyncBroker) -> None:
    task_broker.register_task(create_diary_cards_report, "create_diary_cards_report")
