from dataclasses import dataclass

from src.diary_ms.domain.common.model.commands.commands import Command


@dataclass
class CreateEmotionAdminCommand(Command[None]):
    name: str
    description: str | None = None
