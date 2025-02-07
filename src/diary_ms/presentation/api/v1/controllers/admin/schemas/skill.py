from pydantic import BaseModel

from src.diary_ms.domain.model.value_objects.skill.type import SkillType


class CreateSkillAdminReq(BaseModel):
    name: str
    category: str | None = None
    group: str | None = None
    type: SkillType = SkillType.DBT
    description: str | None = None


class UpdateSkillAdminReq(BaseModel):
    name: str | None = None
    category: str | None = None
    group: str | None = None
    type: SkillType | None = None
    description: str | None = None
