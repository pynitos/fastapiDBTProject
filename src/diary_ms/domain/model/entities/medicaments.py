from typing import NewType

from src.diary_ms.domain.common.types.id import TypeId
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.entities.user_id import UserId

MedicamentId = NewType('MedicamentId', TypeId)


class Medicament(BaseEntity):
    id: MedicamentId
    user_id: UserId
    name: str
    dosage: str
