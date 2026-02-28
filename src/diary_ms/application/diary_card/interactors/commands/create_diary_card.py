from uuid import UUID, uuid4

from diary_ms.application.common.interfaces.dispatcher.base import Publisher
from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from diary_ms.application.diary_card.interfaces.gateway import DiaryCardSaver
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
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.intensity import UrgeIntensity
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class CreateDiaryCard(CommandHandler[CreateDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: DiaryCardSaver,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager
        self._publisher = publisher

    async def __call__(self, command: CreateDiaryCardCommand) -> None:
        id: UUID = uuid4()
        user_id: UserId = self._id_provider.get_current_user_id()
        skills: list[SkillApplication] = (
            [
                SkillApplication(
                    diary_card_id=DiaryCardId(id),
                    skill_id=SkillId(s.id),
                    usage=SkillUsage(s.skill_usage) if s.skill_usage else None,
                    effectiveness=SkillEffectiveness(s.effectiveness) if s.effectiveness else None,
                )
                for s in command.skills
            ]
            if command.skills
            else []
        )
        targets: list[CopingStrategy] = (
            [
                CopingStrategy(
                    diary_card_id=DiaryCardId(id),
                    target_id=TargetId(t.target_id),
                    urge_intensity=UrgeIntensity(t.urge_intensity) if t.urge_intensity else None,
                    action=CopingAction(t.action) if t.action else None,
                    effectiveness=SkillEffectiveness(t.effectiveness) if t.effectiveness else None,
                )
                for t in command.targets
            ]
            if command.targets
            else []
        )
        diary_card: DiaryCard = DiaryCard.create(
            mood=DCMood(command.mood),
            id=DiaryCardId(id),
            user_id=user_id,
            description=DCDescription(command.description),
            date_of_entry=DCDateOfEntry(command.date_of_entry),
            targets=targets,
            emotions=command.emotions,
            medicaments=command.medicaments,
            skills=skills,
            skill_type=command.skills_type,
        )
        await self._db_gateway.create(diary_card)
        await self._publisher.publish(diary_card.pull_events())
        await self._transaction_manager.commit()
