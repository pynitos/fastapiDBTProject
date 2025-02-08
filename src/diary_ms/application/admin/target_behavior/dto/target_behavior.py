from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query


@dataclass
class TargetAdminDTO(DTO):
    id: UUID
    urge: str
    action: str


@dataclass
class GetTargetAdminDTO(Query[TargetAdminDTO]):
    id: UUID


@dataclass
class GetTargetsAdminDTO(Query[list[TargetAdminDTO]]):
    pagination: Pagination
