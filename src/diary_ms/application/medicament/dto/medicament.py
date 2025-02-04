from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO


@dataclass
class MedicamentDTO(DTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str
