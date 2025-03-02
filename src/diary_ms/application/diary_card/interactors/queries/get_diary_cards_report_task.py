from dataclasses import dataclass

from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.task_sender import TaskSender
from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader


@dataclass
class GetDiaryCardsReportTaskQuery(Query):
    task_id: str


class GetDiaryCardsReportTaskHandler(QueryHandler[GetDiaryCardsReportTaskQuery, DiaryCardsReportDTO]):
    def __init__(self, db_gateway: DiaryCardReader, id_provider: IdProvider, task_sender: TaskSender) -> None:
        self.db_gateway = db_gateway
        self._id_provider = id_provider
        self._task_sender = task_sender

    async def __call__(self, query: GetDiaryCardsReportTaskQuery) -> DiaryCardsReportDTO:
        self._id_provider.get_current_user_id()
        result = await self._task_sender.get_result(query.task_id)
        dto = DiaryCardsReportDTO(total=result.total)
        return dto
