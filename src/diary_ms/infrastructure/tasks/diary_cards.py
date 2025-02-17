import logging

from dishka.integrations.taskiq import inject

logger = logging.getLogger(__name__)


@inject
async def create_diary_cards_report() -> str:
    result: str = "Diary Cards report task done."
    logger.info(result)
    return result
