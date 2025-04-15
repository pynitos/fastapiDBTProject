from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query


@dataclass
class OwnTargetDTO(DTO):
    id: UUID
    urge: str
    action: str


@dataclass
class GetOwnTargetQuery(Query[OwnTargetDTO]):
    id: UUID


@dataclass
class GetOwnAndDefaultTargetsQuery(Query[list[OwnTargetDTO]]):
    pagination: Pagination


@dataclass
class GetOwnTargetsQuery(Query[list[OwnTargetDTO]]):
    pagination: Pagination
