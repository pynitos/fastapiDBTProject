from abc import abstractmethod
from typing import Protocol

from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO


class ReportGenerator(Protocol):
    @abstractmethod
    async def generate(self, report_data: DiaryCardsReportDTO) -> bytes:
        raise NotImplementedError
