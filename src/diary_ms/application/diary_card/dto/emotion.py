from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.pagination import Pagination


@dataclass
class EmotionDTO:
    id: UUID
    name: str
    description: str | None


@dataclass
class GetEmotionsDTO:
    pagination: Pagination
