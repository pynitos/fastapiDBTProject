import logging

from dishka.integrations.taskiq import FromDishka, inject

from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.main.config import Settings

logger = logging.getLogger(__name__)


@inject
async def create_diary_cards_report(config: FromDishka[Settings]) -> DiaryCardsReportDTO:
    dto = DiaryCardsReportDTO(total=config.API_PREFIX)
    return dto
