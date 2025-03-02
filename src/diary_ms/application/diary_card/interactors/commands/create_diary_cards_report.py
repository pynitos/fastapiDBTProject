from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader


class CreateDiaryCardsReportCommand(Command[DiaryCardsReportDTO]):
    pass


class CreateDiaryCardsReport(CommandHandler[CreateDiaryCardsReportCommand, DiaryCardsReportDTO]):
    def __init__(
        self,
        db_gateway: DiaryCardReader,
    ) -> None:
        self._db_gateway = db_gateway

    async def __call__(self, command: CreateDiaryCardsReportCommand) -> DiaryCardsReportDTO:
        return DiaryCardsReportDTO("fefe")
