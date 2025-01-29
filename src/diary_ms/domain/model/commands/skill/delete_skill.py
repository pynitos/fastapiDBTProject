from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.commands.base import Command


@dataclass
class DeleteSkillAdminCommand(Command):
    id: UUID
