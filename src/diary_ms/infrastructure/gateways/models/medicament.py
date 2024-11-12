from uuid import UUID

from src.diary_ms.infrastructure.gateways.models.base import Base


class Medicament(Base, table=True):
    user_id: UUID
    name: str
    dosage: str
