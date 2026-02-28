from dataclasses import dataclass

from diary_ms.application.common.dto.command import Command
from diary_ms.domain.common.types.id import TypeId


@dataclass
class UpdateMedicamentCommand(Command[None]):
    id: TypeId
    name: str | None
    dosage: str | None


@dataclass
class UpdateMedicamentAdminCommand(Command[None]):
    id: TypeId
    name: str | None
    dosage: str | None
