from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from src.diary_ms.domain.model.value_objects.medicament.name import MedicamentName


@dataclass
class Medicament(BaseEntity):
    user_id: UserId
    name: MedicamentName
    dosage: MedicamentDosage
    id: MedicamentId = MedicamentId(None)

    @classmethod
    def create(
        cls,
        id: MedicamentId,
        user_id: UserId,
        name: MedicamentName,
        dosage: MedicamentDosage,
    ) -> Self:
        if not user_id.value:
            raise UserIdNotProvidedError
        medicament = cls(
            id=id,
            user_id=user_id,
            name=name,
            dosage=dosage,
        )
        return medicament

    def update(self, name: MedicamentName | None = None, dosage: MedicamentDosage | None = None) -> Self:
        if name:
            self.name = name
        if dosage:
            self.dosage = dosage
        return self
