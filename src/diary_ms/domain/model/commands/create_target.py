from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class CreateTargetCommand(Command[None]):
    urge: str
    action: str
    user_id: UUID
    id: UUID | None = None
