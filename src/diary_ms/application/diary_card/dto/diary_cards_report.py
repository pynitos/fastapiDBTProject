from dataclasses import dataclass

from src.diary_ms.application.common.dto.base import DTO


@dataclass
class DiaryCardsReportDTO(DTO):
    total: str
