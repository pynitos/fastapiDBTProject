import logging

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.exceptions.base import GatewayError
from src.diary_ms.application.diary_card.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardDTOForUpdateReader,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
)
from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.infrastructure.gateways.sqla.db.tables import (
    emotions_table,
    medicaments_table,
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

    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[DiaryCard]:
        stmt: Select[tuple[DiaryCard]] = (
            select(self._db_model).where(self._db_model.user_id == user_id).offset(offset).limit(limit)
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
