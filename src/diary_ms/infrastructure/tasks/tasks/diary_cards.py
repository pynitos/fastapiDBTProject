import logging

from dishka.integrations.taskiq import FromDishka, inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.interactors.commands.create_diary_cards_report import (
    CreateDiaryCardsReportCommand,
)

logger = logging.getLogger(__name__)


@inject
async def create_diary_cards_report(sender: FromDishka[Sender]) -> DiaryCardsReportDTO:
    return await sender.send_command(CreateDiaryCardsReportCommand())
