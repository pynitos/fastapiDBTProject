from dataclasses import dataclass

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from src.diary_ms.domain.model.value_objects.medicament.name import MedicamentName


@dataclass
class MedicamentDM(BaseEntity):
    id: MedicamentId
    user_id: UserId
    name: MedicamentName
    dosage: MedicamentDosage

    @classmethod
    def create(cls, command: CreateMedicamentCommand):
        medicament = cls(
            id=command.id,
            user_id=command.user_id,
            name=MedicamentName(command.name),
            dosage=MedicamentDosage(command.dosage),
        )
        return medicament
