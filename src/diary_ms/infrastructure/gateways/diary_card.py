import logging
from uuid import UUID

from sqlalchemy.engine import TupleResult
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.diary_ms.application.common.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.application.dto.diary_card import (
    OwnDiaryCardDTO,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.infrastructure.gateways.base import BaseGateway
from src.diary_ms.infrastructure.gateways.converters.diary_card import DiaryCardMapper
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
from src.diary_ms.infrastructure.gateways.models.skill import Skill
from src.diary_ms.infrastructure.gateways.models.target import Target

logger = logging.getLogger(__name__)


class DiaryCardGateway(BaseGateway[DiaryCard, DiaryCardDM]):
    _mapper: type[DiaryCardMapper] = DiaryCardMapper

    async def _get_attrs_by_entity(self, entity: DiaryCardDM):
        """Get targets, emotions, medicaments and skills."""
        targets, emotions, medicaments, skills = None, None, None, None
        if entity.targets:
            targets: list[Target] = (
                await self._session.exec(select(Target).where(id in entity.targets))
            ).all()
        if entity.emotions:
            emotions: list[Emotion] = (
                await self._session.exec(select(Emotion).where(id in entity.emotions))
            ).all()
        if entity.medicaments:
            medicaments: list[Medicament] = (
                await self._session.exec(
                    select(Medicament).where(id in entity.medicaments)
                )
            ).all()
        if entity.skills:
            skills: list[Skill] = (
                await self._session.exec(select(Skill).where(id in entity.skills))
            ).all()
        return targets, emotions, medicaments, skills

    async def create(self, entity: DiaryCardDM) -> None:
        targets, emotions, medicaments, skills = await self._get_attrs_by_entity(entity)
        db_entity: DiaryCard = DiaryCard(
            user_id=entity.user_id,
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

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCardDM]:
        stmt: SelectOfScalar = select(self._db_model).offset(offset).limit(limit)
        result: TupleResult = await self._session.exec(stmt)
        result_list: list[DiaryCard] = result.all()
        dto_list: list[OwnDiaryCardDTO] = self._mapper.db_list_to_dto_list(result_list)
        return dto_list

    async def _get_by_id(self, pk: UUID) -> DiaryCard | None:
        return await self._session.get(self._db_model, pk)

    async def get_by_id(self, pk: UUID) -> OwnDiaryCardDTO | None:
        entity: DiaryCard | None = await self._get_by_id(pk=pk)
        if not entity:
            return None
        return self._mapper.db_to_dm(entity)

    async def get_dto_by_id(self, pk: UUID) -> OwnDiaryCardDTO | None:
        entity: DiaryCard | None = await self._get_by_id(pk=pk)
        if not entity:
            return None
        return self._mapper.db_to_dto(entity)

    async def update(self, entity: DiaryCardDM) -> None:
        pk = entity.id
        db_entity: DiaryCard = await self._get_by_id(pk)
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
            db_entity.targets = targets
        if entity.emotions:
            db_entity.emotions = emotions
        if entity.medicaments:
            db_entity.medicaments = medicaments
        if entity.skills:
            db_entity.skills = skills

        self._session.add(db_entity)

    async def delete(self, pk: DiaryCardId) -> None:
        entity: DiaryCard | None = await self._session.get(self._db_model, pk)
        if not entity:
            raise DiaryCardNotFoundError
        await self._session.delete(entity)
