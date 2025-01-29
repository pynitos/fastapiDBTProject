from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.pagination import Pagination


@dataclass
class EmotionDTO(DTO):
    id: UUID
    name: str
    description: str | None


@dataclass
class GetEmotionsDTO(DTO):
    pagination: Pagination
