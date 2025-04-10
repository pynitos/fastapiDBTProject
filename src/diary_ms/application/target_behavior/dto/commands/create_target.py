from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class CreateTargetCommand(Command[None]):
    urge: str
    action: str | None = None
    user_id: UUID | None = None
    id: UUID | None = None


@dataclass
class CreateTargetAdminCommand(Command[None]):
    urge: str
    action: str
    user_id: UUID | None = None
    id: UUID | None = None
    is_default: bool = False
