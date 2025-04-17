from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query


@dataclass
class MedicamentAdminDTO(ResultDTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str


@dataclass
class GetMedicamentAdminDTO(Query[MedicamentAdminDTO]):
    id: UUID


@dataclass
class GetMedicamentsAdminDTO(Query[list[MedicamentAdminDTO]]):
    pagination: Pagination
