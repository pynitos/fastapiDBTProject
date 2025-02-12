from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class DeleteEmotionAdminCommand(Command[None]):
    id: UUID
