from uuid import UUID

from src.diary_ms.infrastructure.gateways.models.base import Base


class Target(Base, table=True):
    user_id: UUID
    urge: str
    action: str
