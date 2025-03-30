import logging
from typing import Any

from sqlalchemy import Row, ScalarResult, Select, func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.exceptions.base import GatewayError
from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
)
from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from src.diary_ms.infrastructure.gateways.sqla.db.tables import (
    diary_cards_table,
    emotions_table,
    medicaments_table,
)

logger = logging.getLogger(__name__)


class DiaryCardGateway(
    DiaryCardReader,
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
        if coping_strategies := entity.coping_strategies:
            for t in coping_strategies:
                id: str = str(t.target_id.value)
                if not await self._session.get(Target, id):
                    raise GatewayError(f"Target with id: {id} not found.", 404)
        if entity.emotions_ids:
            entity.emotions = list(
                (await self._session.scalars(select(Emotion).where(emotions_table.c.id.in_(entity.emotions_ids)))).all()
            )
        if entity.medicaments_ids:
            entity.medicaments = list(
                (
                    await self._session.scalars(
                        select(Medicament).where(medicaments_table.c.id.in_(entity.medicaments_ids))
                    )
                ).all()
            )
        if entity.skill_usages:
            for s in entity.skill_usages:
                id: str = str(s.skill_id.value)
                if not await self._session.get(Skill, id):
                    raise GatewayError(f"Skill with id: {id} not found.", 404)

    async def create(self, entity: DiaryCard) -> None:
        await self._set_entity_relationships(entity)
        self._session.add(entity)

    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[DiaryCard]:
        stmt: Select[tuple[DiaryCard]] = (
            select(self._db_model)
            .where(diary_cards_table.c.user_id == user_id.value)
            .order_by(diary_cards_table.c.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result: ScalarResult[DiaryCard] = await self._session.scalars(stmt)
        result_list: list[DiaryCard] = list(result.all())
        return result_list

    async def get_by_id(self, id: DiaryCardId, user_id: UserId) -> DiaryCard | None:
        if not id.value:
            raise GatewayError("Diary card id not provided", 400)
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[DiaryCard]] = select(self._db_model).where(
            self._db_model.id == id,  # type: ignore
            self._db_model.user_id == user_id,  # type: ignore
        )
        result: ScalarResult[DiaryCard] = await self._session.scalars(stmt)
        entity: DiaryCard | None = result.first()
        return entity

    async def update(self, entity: DiaryCard) -> None:
        await self._set_entity_relationships(entity)
        self._session.add(entity)

    async def delete(self, id: DiaryCardId, user_id: UserId) -> None:
        entity: DiaryCard | None = await self.get_by_id(id, user_id)
        if not entity:
            raise DiaryCardNotFoundError
        await self._session.delete(entity)

    async def generate_report_data(
        self,
        user_id: UserId,
        start_date: DCDateOfEntry,
        end_date: DCDateOfEntry,
    ) -> DiaryCardsReportDTO:
        stmt = (
            select(
                func.count(diary_cards_table.c.id).label("total_entries"),
                func.avg(diary_cards_table.c.mood).label("average_mood"),
            )
            .where(diary_cards_table.c.user_id == user_id.value)
            .where(diary_cards_table.c.date_of_entry >= start_date.value)
            .where(diary_cards_table.c.date_of_entry <= end_date.value)
        )
        result = await self._session.execute(stmt)
        row: Row[tuple[int, Any]] | None = result.first()

        total_entries = row.total_entries if row else 0
        row_average_mood = row.average_mood if row else 0
        average_mood = row_average_mood if row_average_mood else 0
        return DiaryCardsReportDTO(
            start_date=start_date.value,
            end_date=end_date.value,
            total_entries=total_entries,
            average_mood=average_mood,
        )
