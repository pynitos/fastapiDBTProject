from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class CreateTargetCommand(Command[None]):
    urge: str
    action: str
    user_id: UUID | None = None
    id: UUID | None = None


@dataclass
class CreateTargetAdminCommand(Command[None]):
    urge: str
    action: str
    user_id: UUID | None = None
    id: UUID | None = None
    is_default: bool = False
