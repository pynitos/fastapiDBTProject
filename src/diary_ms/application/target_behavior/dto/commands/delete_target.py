from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class DeleteTargetCommand(Command[None]):
    id: UUID


@dataclass
class DeleteTargetAdminCommand(Command[None]):
    id: UUID
