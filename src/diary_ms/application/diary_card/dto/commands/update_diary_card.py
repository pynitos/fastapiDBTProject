from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class UpdateDiaryCardCommand(Command[None]):
    @dataclass
    class Skill:
        id: UUID
        usage: str | None = None
        effectiveness: int | None = None

    id: UUID
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[UUID] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills_type: SkillType | None = SkillType.DBT
    skills: list[Skill] | None = None
