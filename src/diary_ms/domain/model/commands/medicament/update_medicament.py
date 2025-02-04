from dataclasses import dataclass

from src.diary_ms.domain.common.model.commands.commands import Command
from src.diary_ms.domain.common.types.id import TypeId


@dataclass
class UpdateMedicamentCommand(Command[None]):
    id: TypeId
    name: str | None
    dosage: str | None
