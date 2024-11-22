from dataclasses import dataclass

from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


@dataclass
class DeleteDiaryCardCommand:
    id: DiaryCardId
