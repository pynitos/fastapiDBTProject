import logging

from diary_ms.application.common.exceptions.base import AuthorizationError
from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.diary_card.dto.commands.update_diary_card import UpdateDiaryCardCommand
from diary_ms.application.diary_card.interfaces.gateway import DiaryCardUpdater
from diary_ms.domain.model.aggregates.diary_card import DiaryCard
from diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from diary_ms.domain.model.entities.coping_strategy import CopingStrategy
from diary_ms.domain.model.entities.skill_application import SkillApplication
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from diary_ms.domain.model.value_objects.skill.effectiveness import SkillEffectiveness
from diary_ms.domain.model.value_objects.skill.id import SkillId
from diary_ms.domain.model.value_objects.skill.situation import SkillUsage
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.intensity import UrgeIntensity
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId

logger = logging.getLogger()


class UpdateDiaryCard(CommandHandler[UpdateDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: DiaryCardUpdater,
        id_provider: IdProvider,
        uow: TransactionManager,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, command: UpdateDiaryCardCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        old_diary_card: DiaryCard | None = await self.db_gateway.get_by_id(DiaryCardId(command.id), user_id)
        if old_diary_card:
            if old_diary_card.user_id != user_id:
                raise AuthorizationError()
            skill_applications = (
                [
                    SkillApplication(
                        diary_card_id=old_diary_card.id,
                        skill_id=SkillId(s.id),
                        usage=SkillUsage(s.usage) if s.usage else None,
                        effectiveness=SkillEffectiveness(s.effectiveness) if s.effectiveness else None,
                    )
                    for s in command.skills
                ]
                if command.skills
                else None
            )
            coping_strategies = (
                [
                    CopingStrategy(
                        diary_card_id=old_diary_card.id,
                        target_id=TargetId(cs.target_id),
                        urge_intensity=UrgeIntensity(cs.urge_intensity) if cs.urge_intensity else None,
                    )
                    for cs in command.targets
                ]
                if command.targets
                else None
            )
            updated_diary_card: DiaryCard = old_diary_card.update(
                mood=DCMood(command.mood) if command.mood else None,
                description=DCDescription(command.description) if command.description else None,
                date_of_entry=DCDateOfEntry(command.date_of_entry) if command.date_of_entry else None,
                targets=coping_strategies,
                emotions=command.emotions,
                medicaments=command.medicaments,
                skills=skill_applications,
                skill_type=command.skills_type,
            )
            await self.db_gateway.update(updated_diary_card)
            logger.debug(f"Diary card with id: {command.id} updated.")
            await self.uow.commit()
