from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query


@dataclass
class OwnMedicamentDTO(ResultDTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str


@dataclass
class GetOwnMedicamentDTO(Query[OwnMedicamentDTO]):
    id: UUID


@dataclass
class GetOwnMedicamentsDTO(Query[list[OwnMedicamentDTO]]):
    pagination: Pagination
