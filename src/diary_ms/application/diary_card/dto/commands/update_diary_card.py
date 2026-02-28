from dataclasses import dataclass
from datetime import date
from uuid import UUID

from diary_ms.application.common.dto.command import Command
from diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class UpdateCopingStrategyCommand:
    target_id: UUID
    urge_intensity: int | None = None
    action: str | None = None
    effectiveness: int | None = None


@dataclass
class UpdateSkillApplicationCommand:
    id: UUID
    usage: str | None = None
    effectiveness: int | None = None


@dataclass
class UpdateDiaryCardCommand(Command[None]):
    id: UUID
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[UpdateCopingStrategyCommand] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills_type: SkillType | None = SkillType.DBT
    skills: list[UpdateSkillApplicationCommand] | None = None
