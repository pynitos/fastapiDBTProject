from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO


@dataclass
class SkillDTO(DTO):
    id: UUID
    category: str | None
    group: str | None
    name: str
