from src.diary_ms.application.diary_card.dto.skill import SkillDTO
from src.diary_ms.application.diary_card.exceptions.skill import SkillIdNotProvidedError
from src.diary_ms.domain.model.entities.skill import Skill


class SkillDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Skill) -> SkillDTO:
        if not dm.id.value:
            raise SkillIdNotProvidedError
        return SkillDTO(
            id=dm.id.value,
            category=dm.category.value if dm.category else None,
            group=dm.group.value if dm.group else None,
            name=dm.name.value,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Skill]) -> list[SkillDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
