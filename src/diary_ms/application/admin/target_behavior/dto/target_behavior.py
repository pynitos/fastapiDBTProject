from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query


@dataclass
class TargetAdminDTO(ResultDTO):
    id: UUID
    urge: str
    action: str | None


@dataclass
class GetTargetAdminDTO(Query[TargetAdminDTO]):
    id: UUID


@dataclass
class GetTargetsAdminDTO(Query[list[TargetAdminDTO]]):
    pagination: Pagination
