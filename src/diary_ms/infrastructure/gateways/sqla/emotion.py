from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.diary_card.interfaces.gateway import EmotionReader
from src.diary_ms.domain.model.entities.emotion import Emotion


class EmotionGateway(EmotionReader):
    def __init__(
        self,
        db_model: type[Emotion],
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._db_model = db_model

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Emotion]:
        stmt: Select[tuple[Emotion]] = select(self._db_model).offset(offset).limit(limit)
        result: ScalarResult[Emotion] = await self._session.scalars(stmt)
        result_list: list[Emotion] = list(result.all())
        return result_list
