from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class CreateMedicamentCommand(Command[None]):
    name: str
    dosage: str
    user_id: UUID
    id: UUID | None = None
