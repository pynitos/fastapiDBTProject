from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge


class TargetAdminService:
    def create_target(
        self,
        id: TargetId,
        user_id: UserId,
        urge: TargetUrge,
        action: CopingAction,
        is_default: TargetIsDefault,
    ) -> Target:
        if not user_id.value:
            raise UserIdNotProvidedError
        t = Target(
            id=id,
            user_id=user_id,
            urge=urge,
            action=action,
            is_default=is_default,
        )
        return t
