from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query


@dataclass
class OwnTargetDTO(ResultDTO):
    id: UUID
    urge: str
    action: str | None


@dataclass
class GetOwnTargetQuery(Query[OwnTargetDTO]):
    id: UUID


@dataclass
class GetOwnAndDefaultTargetsQuery(Query[list[OwnTargetDTO]]):
    pagination: Pagination


@dataclass
class GetOwnTargetsQuery(Query[list[OwnTargetDTO]]):
    pagination: Pagination
