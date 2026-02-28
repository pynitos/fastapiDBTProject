from dataclasses import dataclass, field
from uuid import UUID

from diary_ms.application.common.dto.base import ResultDTO
from diary_ms.application.common.dto.pagination import Pagination
from diary_ms.application.common.dto.query import Query


@dataclass
class OwnMedicamentDTO(ResultDTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str


@dataclass
class OwnMedicamentsDTO(ResultDTO):
    medicaments: list[OwnMedicamentDTO] = field(default_factory=list)
    total: int = 0


@dataclass
class GetOwnMedicamentDTO(Query[OwnMedicamentDTO]):
    id: UUID


@dataclass
class GetOwnMedicamentsDTO(Query[OwnMedicamentsDTO]):
    pagination: Pagination
