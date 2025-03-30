from uuid import UUID, uuid4

from src.diary_ms.application.common.interfaces.dispatcher.base import Publisher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardSaver
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.coping_strategy import CopingStrategy
from src.diary_ms.domain.model.entities.diary_card_skill import SkillUsage
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.situation import SkillSituation
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.effectiveness import CopingEffectiveness
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


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
        skills: list[SkillUsage] = (
            [
                SkillUsage(
                    diary_card_id=DiaryCardId(id),
                    skill_id=SkillId(s.id),
                    situation=SkillSituation(s.situation),
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
                    action=CopingAction(t.action),
                    effectiveness=CopingEffectiveness(t.effectiveness)
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
