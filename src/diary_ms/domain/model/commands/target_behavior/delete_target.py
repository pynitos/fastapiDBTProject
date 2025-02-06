from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class DeleteTargetCommand(Command[None]):
    id: UUID
