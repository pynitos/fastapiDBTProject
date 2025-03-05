from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.application.common.interfaces.file_manager import FileManager
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from src.diary_ms.application.diary_card.interfaces.report_generator import ReportGenerator
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry


@dataclass
class CreateDiaryCardsReportCommand(Command[DiaryCardsReportDTO]):
    user_id: UUID


class CreateDiaryCardsReport(CommandHandler[CreateDiaryCardsReportCommand, DiaryCardsReportDTO]):
    def __init__(
        self,
        db_gateway: DiaryCardReader,
        report_generator: ReportGenerator,
        file_manager: FileManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._report_generator = report_generator
        self._file_manager = file_manager

    async def __call__(self, command: CreateDiaryCardsReportCommand) -> DiaryCardsReportDTO:
        today: date = date.today()
        start_of_week: date = today - timedelta(days=today.weekday())
        report: DiaryCardsReportDTO = await self._db_gateway.generate_report_data(
            user_id=UserId(command.user_id), start_date=DCDateOfEntry(start_of_week), end_date=DCDateOfEntry(today)
        )
        pdf_report = await self._report_generator.generate(report)
        file_path = f"reports/{command.user_id}_{report.start_date.strftime('%Y-%m-%d')}_{report.end_date.strftime('%Y-%m-%d')}.pdf"
        self._file_manager.save(pdf_report, file_path)
        report.file_path = file_path
        return report
