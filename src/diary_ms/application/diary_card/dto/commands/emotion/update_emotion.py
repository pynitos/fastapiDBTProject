from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class UpdateEmotionAdminCommand(Command[None]):
    id: UUID
    name: str | None = None
    description: str | None = None
