from dataclasses import dataclass

from diary_ms.application.common.dto.command import Command


@dataclass
class CreateEmotionAdminCommand(Command[None]):
    name: str
    description: str | None = None
