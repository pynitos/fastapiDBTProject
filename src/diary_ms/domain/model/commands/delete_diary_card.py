from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from dataclasses import dataclass

@dataclass
class DeleteDiaryCardCommand:
    id: DiaryCardId
