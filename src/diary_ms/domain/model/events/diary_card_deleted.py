from dataclasses import dataclass
from datetime import date
from typing import ClassVar
from uuid import UUID

from src.diary_ms.domain.common.model.events.base import BaseEvent


@dataclass(frozen=True)
class DiaryCardCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = "New Diary Card Received"

    diary_card_id: UUID
    user_id: UUID
    date_of_entry: date
    type: str
