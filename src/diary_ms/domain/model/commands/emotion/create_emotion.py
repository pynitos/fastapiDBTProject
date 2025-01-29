from dataclasses import dataclass

from src.diary_ms.domain.common.model.commands.base import Command


@dataclass
class CreateEmotionAdminCommand(Command):
    name: str
    description: str | None = None
