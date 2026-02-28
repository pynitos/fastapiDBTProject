from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from diary_ms.application.common.dto.command import Command
from diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class CreateCopingStrategyCommand:
    target_id: UUID
    urge_intensity: int | None = None
    action: str | None = None
    effectiveness: int | None = None


@dataclass
class CreateSkillApplicationCommand:
    id: UUID
    skill_usage: str | None = None
    effectiveness: int | None = None


@dataclass
class CreateDiaryCardCommand(Command[None]):
    mood: int
    id: UUID | None = None
    user_id: UUID | None = None
    description: str | None = None
    date_of_entry: date = field(default_factory=date.today)

    targets: list[CreateCopingStrategyCommand] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[CreateSkillApplicationCommand] | None = None

    skills_type: SkillType = SkillType.DBT
