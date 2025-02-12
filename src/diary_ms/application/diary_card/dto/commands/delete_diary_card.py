from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class DeleteDiaryCardCommand(Command[None]):
    id: UUID


@dataclass
class DeleteDiaryCardAdminCommand(Command[None]):
    id: UUID
