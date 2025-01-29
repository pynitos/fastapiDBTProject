from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.pagination import Pagination


@dataclass
class EmotionAdminDTO(DTO):
    id: UUID
    name: str
    description: str | None


@dataclass
class GetEmotionAdminDTO(DTO):
    id: UUID


@dataclass
class GetEmotionsAdminDTO(DTO):
    pagination: Pagination
