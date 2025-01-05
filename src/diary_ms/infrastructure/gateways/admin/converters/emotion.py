from collections.abc import Sequence

from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion


class EmotionAdminMapper:
    @classmethod
    def db_list_to_dto_list(cls, db_list: Sequence[Emotion]) -> list[EmotionAdminDTO]:
        dto_list: list[EmotionAdminDTO] = []
        for entity in db_list:
            dto_entity: EmotionAdminDTO = cls.db_to_dto(entity)
            dto_list.append(dto_entity)
        return dto_list

    @classmethod
    def db_to_dto(cls, entity: Emotion) -> EmotionAdminDTO:
        return EmotionAdminDTO(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )

    @classmethod
    def db_to_dm(cls, entity: Emotion) -> EmotionDM:
        domain_entity: EmotionDM = EmotionDM(
            id=EmotionId(entity.id),
            name=EmotionName(entity.name),
            description=EmotionDescription(entity.description),
        )
        return domain_entity
