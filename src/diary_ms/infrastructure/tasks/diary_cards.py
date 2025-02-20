import logging

from src.diary_ms.infrastructure.tasks.brokers.broker import task_broker

logger = logging.getLogger(__name__)


@task_broker.task
async def create_diary_cards_report() -> str:
    result: str = "Diary Cards report task done."
    logger.info(result)
    return result
