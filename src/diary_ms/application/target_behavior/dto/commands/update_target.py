from dataclasses import dataclass
from uuid import UUID

from diary_ms.application.common.dto.command import Command


@dataclass
class UpdateTargetCommand(Command[None]):
    target_id: UUID
    urge: str | None = None
    action: str | None = None
    user_id: UUID | None = None


@dataclass
class UpdateTargetAdminCommand(Command[None]):
    target_id: UUID
    urge: str | None = None
    action: str | None = None
    user_id: UUID | None = None
