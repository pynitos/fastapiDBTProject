from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class DeleteSkillAdminCommand(Command[None]):
    id: UUID
