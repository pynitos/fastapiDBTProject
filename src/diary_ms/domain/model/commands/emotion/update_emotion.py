from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.base import Command


@dataclass
class UpdateEmotionAdminCommand(Command):
    id: UUID
    name: str | None = None
    description: str | None = None
