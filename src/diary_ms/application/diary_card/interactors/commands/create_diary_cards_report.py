from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry


@dataclass
class CreateDiaryCardsReportCommand(Command[DiaryCardsReportDTO]):
    user_id: UUID


class CreateDiaryCardsReport(CommandHandler[CreateDiaryCardsReportCommand, DiaryCardsReportDTO]):
    def __init__(
        self,
        db_gateway: DiaryCardReader,
    ) -> None:
        self._db_gateway = db_gateway

    async def __call__(self, command: CreateDiaryCardsReportCommand) -> DiaryCardsReportDTO:
        today: date = date.today()
        start_of_week: date = today - timedelta(days=today.weekday())
        report: DiaryCardsReportDTO = await self._db_gateway.generate_report_data(
            user_id=UserId(command.user_id), start_date=DCDateOfEntry(start_of_week), end_date=DCDateOfEntry(today)
        )
        return report
