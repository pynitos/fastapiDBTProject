from src.diary_ms.application.admin.target_behavior.dto.target_behavior import TargetAdminDTO
from src.diary_ms.application.target_behavior.exceptions.target_behavior import TargetIdNotProvidedError
from src.diary_ms.domain.model.entities.target_behavior import Target


class TargetAdminDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Target) -> TargetAdminDTO:
        if not dm.id.value:
            raise TargetIdNotProvidedError
        return TargetAdminDTO(
            id=dm.id.value,
            urge=dm.urge.value,
            action=dm.action.value,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Target]) -> list[TargetAdminDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
