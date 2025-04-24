from src.diary_ms.application.target_behavior.dto.target_behavior import OwnTargetResultDTO
from src.diary_ms.application.target_behavior.exceptions.target_behavior import TargetIdNotProvidedError
from src.diary_ms.domain.model.entities.target_behavior import Target


class TargetDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Target) -> OwnTargetResultDTO:
        if not dm.id.value:
            raise TargetIdNotProvidedError
        return OwnTargetResultDTO(
            id=dm.id.value,
            urge=dm.urge.value,
            action=dm.action.value if dm.action else None,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Target]) -> list[OwnTargetResultDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
