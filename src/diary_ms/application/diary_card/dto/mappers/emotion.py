from diary_ms.application.diary_card.dto.diary_card import EmotionResultDTO
from diary_ms.domain.common.exceptions.base import AppError
from diary_ms.domain.model.entities.emotion import Emotion


class EmotionDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Emotion) -> EmotionResultDTO:
        if not dm.id.value:
            raise AppError("Emotion id not provided!")
        return EmotionResultDTO(
            id=dm.id.value,
            name=dm.name.value,
            description=dm.description.value if dm.description else None,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Emotion]) -> list[EmotionResultDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
