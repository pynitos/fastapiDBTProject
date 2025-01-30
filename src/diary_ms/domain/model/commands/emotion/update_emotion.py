from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class UpdateEmotionAdminCommand(Command[None]):
    id: UUID
    name: str | None = None
    description: str | None = None
