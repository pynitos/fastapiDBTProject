from dataclasses import dataclass

from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.task_sender import TaskSender
from src.diary_ms.domain.common.exceptions.access import AuthenticationError
from src.diary_ms.domain.model.entities.user_id import UserId


@dataclass
class CreateDiaryCardsReportDTO:
    task_id: str


class CreateDiaryCardsReportCommand(Command[CreateDiaryCardsReportDTO]):
    pass


class CreateDiaryCardsReport(CommandHandler[CreateDiaryCardsReportCommand, CreateDiaryCardsReportDTO]):
    def __init__(
        self,
        id_provider: IdProvider,
        task_sender: TaskSender,
    ) -> None:
        self._id_provider = id_provider
        self._task_sender = task_sender

    async def __call__(self, command: CreateDiaryCardsReportCommand) -> CreateDiaryCardsReportDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        if not user_id.value:
            raise AuthenticationError
        task_id: str = await self._task_sender.send_task("create_diary_cards_report")
        return CreateDiaryCardsReportDTO(task_id=task_id)
