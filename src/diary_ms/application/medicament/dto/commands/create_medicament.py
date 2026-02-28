from dataclasses import dataclass
from uuid import UUID

from diary_ms.application.common.dto.command import Command


@dataclass
class CreateMedicamentCommand(Command[None]):
    name: str
    dosage: str
    user_id: UUID | None = None
    id: UUID | None = None


@dataclass
class CreateMedicamentAdminCommand(Command[None]):
    name: str
    dosage: str
    user_id: UUID | None = None
    id: UUID | None = None
