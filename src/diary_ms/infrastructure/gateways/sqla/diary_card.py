import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.exceptions.base import GatewayError, InfraError
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    DiaryCardForUpdateDTO,
    EmotionForUpdDTO,
    MedicamentForUpdDTO,
    SkillForUpdDTO,
    TargetForUpdDTO,
)
from src.diary_ms.application.diary_card.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardDTOForUpdateReader,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.infrastructure.gateways.sqla.db.tables import (
    emotions_table,
    medicaments_table,
    skills_table,
    targets_table,
)

logger = logging.getLogger(__name__)


class DiaryCardGateway(
    DiaryCardReader,
    DiaryCardDTOForUpdateReader,
    DiaryCardSaver,
    DiaryCardUpdater,
    DiaryCardDeleter,
):
    def __init__(
        self,
        db_model: type[DiaryCard],
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._db_model = db_model

    async def _set_entity_relationships(self, entity: DiaryCard) -> None:
        if entity.targets_ids:
            entity.targets = list(
                (
                    await self._session.scalars(select(targets_table).where(targets_table.c.id.in_(entity.targets_ids)))
                ).all()
            )
        if entity.emotions_ids:
            entity.emotions = list(
                (
                    await self._session.scalars(
                        select(emotions_table).where(emotions_table.c.id.in_(entity.emotions_ids))
                    )
                ).all()
            )
        if entity.medicaments_ids:
            entity.medicaments = list(
                (
                    await self._session.scalars(
                        select(Medicament).where(medicaments_table.c.id.in_(entity.medicaments_ids))
                    )
                ).all()
            )
        if entity.skill_assotiations:
            for s in entity.skill_assotiations:
                if not await self._session.get(Skill, s.skill_id.value):
                    raise GatewayError(f"Skill with id: {id} not found.", 404)

    async def create(self, entity: DiaryCard) -> None:
        await self._set_entity_relationships(entity)
        self._session.add(entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCard]:
        stmt: Select[tuple[DiaryCard]] = select(self._db_model).offset(offset).limit(limit)
        result: ScalarResult[DiaryCard] = await self._session.scalars(stmt)
        result_list: list[DiaryCard] = list(result.all())
        return result_list

    async def _get_by_id(self, pk: UUID | None) -> DiaryCard | None:
        if not pk:
            raise InfraError("Diary card id not provided", 400)
        return await self._session.get(self._db_model, pk)

    async def get_by_id(self, id: DiaryCardId) -> DiaryCard | None:
        return await self._get_by_id(pk=id.value)

    async def get_dto_for_update(self, id: DiaryCardId) -> DiaryCardForUpdateDTO:
        dm: DiaryCard | None = await self._get_by_id(id.value)
        if not dm:
            raise DiaryCardNotFoundError
        all_targets: Sequence[Target] | None = (
            (
                await self._session.scalars(
                    select(Target).where(Target.user_id.in_((t.id for t in dm.targets if not isinstance(t, UUID))))  # type: ignore
                )
            ).all()
            if dm.targets
            else None
        )
        all_emotions: Sequence[Emotion] = (await self._session.scalars(select(Emotion))).all()
        all_medicaments: Sequence[Medicament] | None = (
            (
                await self._session.scalars(
                    select(Medicament).where(
                        Medicament.user_id.in_((m.id for m in dm.medicaments if not isinstance(m, UUID)))  # type: ignore
                    )
                )
            ).all()
            if dm.medicaments
            else None
        )
        all_skills: Sequence[Skill] = (
            await self._session.scalars(select(skills_table).where(skills_table.c.type == dm.type))
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
                    id=t.id.value,
                    urge=t.urge.value,
                    action=t.action.value,
                )
                for t in dm.targets
                if t.id.value
            ]
            if dm.targets
            else None,
            emotions=[
                EmotionForUpdDTO(
                    id=e.id.value,
                    name=e.name.value,
                    description=e.description.value,
                )
                for e in dm.emotions
                if e.id.value
            ]
            if dm.emotions
            else None,
            medicaments=[
                MedicamentForUpdDTO(
                    id=m.id.value,
                    name=m.name.value,
                    dosage=m.dosage.value,
                )
                for m in dm.medicaments
                if m.id.value
            ]
            if dm.medicaments
            else None,
            skills=[
                SkillForUpdDTO(
                    id=s.id.value,
                    category=s.category.value,
                    group=s.group.value,
                    name=s.name.value,
                )
                for s in dm.skills
                if s.id.value
            ]
            if dm.skills
            else None,
            # For choice:
            all_targets=[
                TargetForUpdDTO(
                    id=t.id.value,
                    urge=t.urge.value,
                    action=t.action.value,
                )
                for t in all_targets
                if t.id.value
            ]
            if all_targets
            else None,
            all_emotions=[
                EmotionForUpdDTO(
                    id=e.id.value,
                    name=e.name.value,
                    description=e.description.value,
                )
                for e in all_emotions
                if e.id.value
            ]
            if all_emotions
            else None,
            all_medicaments=[
                MedicamentForUpdDTO(
                    id=m.id.value,
                    name=m.name.value,
                    dosage=m.dosage.value,
                )
                for m in all_medicaments
                if m.id.value
            ]
            if all_medicaments
            else None,
            all_skills=[
                SkillForUpdDTO(
                    id=s.id.value,
                    category=s.category.value,
                    group=s.group.value,
                    name=s.name.value,
                )
                for s in all_skills
                if s.id.value
            ]
            if all_skills
            else None,
        )
        return dto

    async def update(self, entity: DiaryCard) -> None:
        await self._set_entity_relationships(entity)
        self._session.add(entity)

    async def delete(self, id: DiaryCardId) -> None:
        entity: DiaryCard | None = await self._get_by_id(id.value)
        if not entity:
            raise DiaryCardNotFoundError
        await self._session.delete(entity)
