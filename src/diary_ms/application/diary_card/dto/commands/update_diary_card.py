from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command


@dataclass
class UpdateDiaryCardCommand(Command[None]):
    @dataclass
    class Skill:
        id: UUID
        situation: str | None = None

    id: UUID
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[UUID] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[Skill] | None = None
