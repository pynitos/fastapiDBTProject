from dataclasses import dataclass, field
from uuid import UUID

from diary_ms.application.common.dto.base import ResultDTO
from diary_ms.application.common.dto.pagination import Pagination
from diary_ms.application.common.dto.query import Query


@dataclass
class OwnTargetResultDTO(ResultDTO):
    id: UUID
    urge: str
    action: str | None = None


@dataclass
class GetOwnTargetQuery(Query[OwnTargetResultDTO]):
    id: UUID


@dataclass
class OwnTargetsResultDTO(ResultDTO):
    targets: list[OwnTargetResultDTO] = field(default_factory=list)
    total: int = 0


@dataclass
class GetOwnAndDefaultTargetsQuery(Query[OwnTargetsResultDTO]):
    pagination: Pagination


@dataclass
class GetOwnTargetsQuery(Query[OwnTargetsResultDTO]):
    pagination: Pagination
