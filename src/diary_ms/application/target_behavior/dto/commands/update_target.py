from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class UpdateTargetCommand(Command[None]):
    urge: str | None = None
    action: str | None = None
    user_id: UUID | None = None
    id: UUID | None = None


@dataclass
class UpdateTargetAdminCommand(Command[None]):
    urge: str | None = None
    action: str | None = None
    user_id: UUID | None = None
    id: UUID | None = None
