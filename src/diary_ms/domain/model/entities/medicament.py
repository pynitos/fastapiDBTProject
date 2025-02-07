from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.medicament.create_medicament import (
    CreateMedicamentAdminCommand,
    CreateMedicamentCommand,
)
from src.diary_ms.domain.model.commands.medicament.update_medicament import (
    UpdateMedicamentAdminCommand,
    UpdateMedicamentCommand,
)
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
    def create(cls, command: CreateMedicamentCommand) -> Self:
        if not command.user_id:
            raise UserIdNotProvidedError
        medicament = cls(
            user_id=UserId(command.user_id),
            name=MedicamentName(command.name),
            dosage=MedicamentDosage(command.dosage),
        )
        return medicament

    @classmethod
    def admin_create(cls, command: CreateMedicamentAdminCommand) -> Self:
        if not command.user_id:
            raise UserIdNotProvidedError
        medicament = cls(
            user_id=UserId(command.user_id),
            name=MedicamentName(command.name),
            dosage=MedicamentDosage(command.dosage),
        )
        return medicament

    def update(self, command: UpdateMedicamentCommand | UpdateMedicamentAdminCommand) -> Self:
        if command.name:
            self.name = MedicamentName(command.name)
        if command.dosage:
            self.dosage = MedicamentDosage(command.dosage)
        return self
