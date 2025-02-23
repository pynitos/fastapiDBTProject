import logging

from dishka.integrations.taskiq import FromDishka, inject

from src.diary_ms.infrastructure.tasks.brokers.broker import task_broker
from src.diary_ms.main.config import Settings

logger = logging.getLogger(__name__)


@task_broker.task
@inject
async def create_diary_cards_report(config: FromDishka[Settings]):
    return config.API_PREFIX
