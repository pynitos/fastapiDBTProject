import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.application.diary_card.dto.diary_card import (
    OwnDiaryCardDTO,
)
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    DiaryCardForUpdateDTO,
    EmotionForUpdDTO,
    MedicamentForUpdDTO,
    SkillForUpdDTO,
    TargetForUpdDTO,
)
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardDTOForUpdateReader,
    DiaryCardDTOReader,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.infrastructure.gateways.converters.diary_card import DiaryCardMapper
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
from src.diary_ms.infrastructure.gateways.models.skill import Skill
from src.diary_ms.infrastructure.gateways.models.target import Target

logger = logging.getLogger(__name__)


class DiaryCardGateway(
    DiaryCardReader,
    DiaryCardDTOReader,
    DiaryCardDTOForUpdateReader,
    DiaryCardSaver,
    DiaryCardUpdater,
    DiaryCardDeleter,
):
    def __init__(
        self,
        db_model: type[DiaryCard],
        domain_model: type[DiaryCardDM],
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._db_model = db_model
        self._domain_model = domain_model
        self._mapper: type[DiaryCardMapper] = DiaryCardMapper

    async def _get_attrs_by_entity(
        self, entity: DiaryCardDM
    ) -> tuple[
        Sequence[Target], Sequence[Emotion], Sequence[Medicament], Sequence[Skill]
    ]:
        """Get targets, emotions, medicaments and skills."""
        targets: Sequence[Target] = []
        emotions: Sequence[Emotion] = []
        medicaments: Sequence[Medicament] = []
        skills: Sequence[Skill] = []
        if entity.targets:
            targets = (
                await self._session.scalars(
                    select(Target).where(Target.id.in_(entity.targets))
                )
            ).all()
        if entity.emotions:
            emotions = (
                await self._session.scalars(
                    select(Emotion).where(Emotion.id.in_(entity.emotions))
                )
            ).all()
        if entity.medicaments:
            medicaments = (
                await self._session.scalars(
                    select(Medicament).where(Medicament.id.in_(entity.medicaments))
                )
            ).all()
        if entity.skills:
            skills = (
                await self._session.scalars(
                    select(Skill).where(Skill.id.in_(entity.skills))
                )
            ).all()
        return targets, emotions, medicaments, skills

    async def create(self, entity: DiaryCardDM) -> None:
        targets, emotions, medicaments, skills = await self._get_attrs_by_entity(entity)
        db_entity: DiaryCard = DiaryCard(
            id=entity.id.value,
            user_id=entity.user_id.value,
            mood=entity.mood.value,
            description=entity.description.value,
            date_of_entry=entity.date_of_entry.value,
            type=entity.type,
            targets=targets,
            emotions=emotions,
            medicaments=medicaments,
            skills=skills,
        )
        self._session.add(db_entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[OwnDiaryCardDTO]:
        stmt: Select[tuple[DiaryCard]] = (
            select(self._db_model).offset(offset).limit(limit)
        )
        result: ScalarResult[DiaryCard] = await self._session.scalars(stmt)
        result_list: Sequence[DiaryCard] = result.all()
        dto_list: list[OwnDiaryCardDTO] = self._mapper.db_list_to_dto_list(result_list)
        return dto_list

    async def _get_by_id(self, pk: UUID | None) -> DiaryCard | None:
        if not pk:
            return None
        return await self._session.get(self._db_model, pk)

    async def get_by_id(self, id: DiaryCardId) -> DiaryCardDM | None:
        entity: DiaryCard | None = await self._get_by_id(pk=id.value)
        if not entity:
            return None
        return self._mapper.db_to_dm(entity)

    async def get_dto_by_id(self, id: DiaryCardId) -> OwnDiaryCardDTO | None:
        entity: DiaryCard | None = await self._get_by_id(pk=id.value)
        if not entity:
            return None
        else:
            dto: OwnDiaryCardDTO = self._mapper.db_to_dto(entity)
            return dto

    async def get_dto_for_update(self, dm: DiaryCardDM) -> DiaryCardForUpdateDTO:
        targets, emotions, medicaments, skills = await self._get_attrs_by_entity(dm)
        all_targets: Sequence[Target] | None = (
            (
                await self._session.scalars(
                    select(Target).where(
                        Target.user_id.in_(
                            (t.id for t in dm.targets if not isinstance(t, UUID))
                        )
                    )
                )
            ).all()
            if dm.targets
            else None
        )
        all_emotions: Sequence[Emotion] = (
            await self._session.scalars(select(Emotion))
        ).all()
        all_medicaments: Sequence[Medicament] | None = (
            (
                await self._session.scalars(
                    select(Medicament).where(
                        Medicament.user_id.in_(
                            (m.id for m in dm.medicaments if not isinstance(m, UUID))
                        )
                    )
                )
            ).all()
            if dm.medicaments
            else None
        )
        all_skills: Sequence[Skill] = (
            await self._session.scalars(select(Skill).where(Skill.type == dm.type))
        ).all()
        if not dm.id.value:
            raise Exception
        dto: DiaryCardForUpdateDTO = DiaryCardForUpdateDTO(
            id=dm.id.value,
            user_id=dm.user_id.value,
            mood=dm.mood.value,
            description=dm.description.value,
            date_of_entry=dm.date_of_entry.value,
            type_=dm.type,
            targets=[
                TargetForUpdDTO(
                    id=t.id,
                    urge=t.urge,
                    action=t.action,
                )
                for t in targets
            ]
            if targets
            else None,
            emotions=[
                EmotionForUpdDTO(
                    id=e.id,
                    name=e.name,
                    description=e.description,
                )
                for e in emotions
                if emotions
            ]
            if emotions
            else None,
            medicaments=[
                MedicamentForUpdDTO(
                    id=m.id,
                    name=m.name,
                    dosage=m.dosage,
                )
                for m in medicaments
                if medicaments
            ]
            if medicaments
            else None,
            skills=[
                SkillForUpdDTO(
                    id=s.id,
                    category=s.category,
                    group=s.group,
                    name=s.name,
                )
                for s in skills
            ]
            if skills
            else None,
            # For choice:
            all_targets=[
                TargetForUpdDTO(
                    id=t.id,
                    urge=t.urge,
                    action=t.action,
                )
                for t in all_targets
            ]
            if all_targets
            else None,
            all_emotions=[
                EmotionForUpdDTO(
                    id=e.id,
                    name=e.name,
                    description=e.description,
                )
                for e in all_emotions
            ]
            if all_emotions
            else None,
            all_medicaments=[
                MedicamentForUpdDTO(
                    id=m.id,
                    name=m.name,
                    dosage=m.dosage,
                )
                for m in all_medicaments
            ]
            if all_medicaments
            else None,
            all_skills=[
                SkillForUpdDTO(
                    id=s.id,
                    category=s.category,
                    group=s.group,
                    name=s.name,
                )
                for s in all_skills
            ]
            if all_skills
            else None,
        )
        return dto

    async def update(self, entity: DiaryCardDM) -> None:
        pk: UUID | None = entity.id.value
        db_entity: DiaryCard | None = await self._get_by_id(pk)
        if not db_entity:
            raise DiaryCardNotFoundError

        targets, emotions, medicaments, skills = await self._get_attrs_by_entity(entity)

        if entity.mood:
            db_entity.mood = entity.mood.value
            logger.debug(f"Update mood with value: {entity.mood.value}")
        if entity.description:
            db_entity.description = entity.description.value
        if entity.date_of_entry:
            db_entity.date_of_entry = entity.date_of_entry.value
        if entity.targets:
            db_entity.targets = list(targets)
        if entity.emotions:
            db_entity.emotions = list(emotions)
        if entity.medicaments:
            db_entity.medicaments = list(medicaments)
        if entity.skills:
            db_entity.skills = list(skills)

        self._session.add(db_entity)

    async def delete(self, id: DiaryCardId) -> None:
        entity: DiaryCard | None = await self._get_by_id(id.value)
        if not entity:
            raise DiaryCardNotFoundError
        await self._session.delete(entity)
