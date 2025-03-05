from dataclasses import dataclass
from datetime import date

from src.diary_ms.application.common.dto.base import DTO


@dataclass
class DiaryCardsReportDTO(DTO):
    start_date: date
    end_date: date
    total_entries: int
    average_mood: int
    file_path: str | None = None
