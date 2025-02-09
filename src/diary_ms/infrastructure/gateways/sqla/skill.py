from uuid import UUID

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.exceptions.base import GatewayError
from src.diary_ms.application.diary_card.interfaces.gateway import SkillReader
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


class SkillGateway(SkillReader):
    def __init__(self, session: AsyncSession, db_model: type[Skill] = Skill) -> None:
        self._session = session
        self._db_model = db_model

    async def get_all(self, type: SkillType, offset: int = 0, limit: int = 10) -> list[Skill]:
        stmt: Select[tuple[Skill]] = (
            select(self._db_model).where(self._db_model.type == type).offset(offset).limit(limit)
        )
        result: ScalarResult[Skill] = await self._session.scalars(stmt)
        result_list: list[Skill] = list(result.all())
        return result_list

    async def get_by_id(self, id: SkillId) -> Skill | None:
        pk: UUID | None = id.value
        if not pk:
            raise GatewayError("Skill id not provided!", 400)
        return await self._session.get(self._db_model, pk)
