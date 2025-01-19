from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from src.diary_ms.domain.model.value_objects.medicament.name import MedicamentName


@dataclass
class Medicament(BaseEntity):
    user_id: UserId
    name: MedicamentName
    dosage: MedicamentDosage
    id: MedicamentId

    @classmethod
    def create(cls, command: CreateMedicamentCommand) -> Self:
        medicament = cls(
            id=MedicamentId(value=None),
            user_id=UserId(command.user_id),
            name=MedicamentName(command.name),
            dosage=MedicamentDosage(command.dosage),
        )
        return medicament
