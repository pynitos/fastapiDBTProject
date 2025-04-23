from src.diary_ms.application.admin.skill.dto.skill import SkillAdminDTO
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.domain.model.entities.skill import Skill


class SkillAdminDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Skill) -> SkillAdminDTO:
        if not dm.id.value:
            raise AppError("Skill id not provided!")
        return SkillAdminDTO(
            id=dm.id.value,
            category=dm.category.value if dm.category else None,
            group=dm.group.value if dm.group else None,
            name=dm.name.value,
            type=dm.type,
            description=dm.description.value if dm.description else None,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Skill]) -> list[SkillAdminDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
