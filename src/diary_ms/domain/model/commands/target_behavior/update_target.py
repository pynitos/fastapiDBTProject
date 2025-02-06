from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class UpdateTargetCommand(Command[None]):
    urge: str | None = None
    action: str | None = None
    user_id: UUID | None = None
    id: UUID | None = None
