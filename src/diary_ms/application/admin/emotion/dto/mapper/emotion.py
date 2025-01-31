from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.domain.model.entities.emotion import Emotion


class EmotionAdminDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Emotion) -> EmotionAdminDTO:
        if not dm.id.value:
            raise AppError("Emotion Id Not Provided!")
        return EmotionAdminDTO(
            id=dm.id.value,
            name=dm.name.value,
            description=dm.description.value,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Emotion]) -> list[EmotionAdminDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
