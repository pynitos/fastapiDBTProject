from taskiq import AsyncBroker

from src.diary_ms.infrastructure.tasks.brokers.dispatcher import TaskDispatcher


def get_task_dispatcher(task_broker: AsyncBroker) -> TaskDispatcher:
    # task_1 = task_broker.register_task(create_diary_cards_report)
    task_dispatcher = TaskDispatcher(task_broker)
    # task_dispatcher.register_task("create_diary_cards_report", create_diary_cards_report)
    return task_dispatcher
