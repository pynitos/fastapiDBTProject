from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class DeleteSkillAdminCommand(Command[None]):
    id: UUID
