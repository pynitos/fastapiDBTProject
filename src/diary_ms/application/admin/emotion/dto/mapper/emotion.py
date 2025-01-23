from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
from src.diary_ms.domain.model.entities.emotion import Emotion


class EmotionAdminMapper:
    @staticmethod
    def dm_to_dto(dm: Emotion) -> EmotionAdminDTO:
        return EmotionAdminDTO(
            id=dm.id.value,
            name=dm.name.value,
            description=dm.description.value,
        )

    @staticmethod
    def dm_list_to_dto_list(dm_list: Emotion) -> list[EmotionAdminDTO]:
        return [
            EmotionAdminDTO(
                id=dm.id.value,
                name=dm.name.value,
                description=dm.description.value,
            )
            for dm in dm_list
        ]
