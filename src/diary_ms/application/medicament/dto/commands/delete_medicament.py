from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class DeleteMedicamentCommand(Command[None]):
    id: UUID


@dataclass
class DeleteMedicamentAdminCommand(Command[None]):
    id: UUID
