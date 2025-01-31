from src.diary_ms.application.diary_card.dto.emotion import EmotionDTO
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.domain.model.entities.emotion import Emotion


class EmotionDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Emotion) -> EmotionDTO:
        if not dm.id.value:
            raise AppError("Emotion id not provided!")
        return EmotionDTO(
            id=dm.id.value,
            name=dm.name.value,
            description=dm.description.value,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Emotion]) -> list[EmotionDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
