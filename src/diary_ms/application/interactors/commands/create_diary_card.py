from uuid import UUID

from src.diary_ms.application.common.interfaces.diary_card import SaverProtocol
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.application.interactors.events.diary_card_created import (
    DiaryCardCreatedEventHandler,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand


class CreateDiaryCard(Interactor[CreateDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: SaverProtocol,
        id_provider: IdProvider,
        uow: UOWProtocol,
        event_handler: DiaryCardCreatedEventHandler,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow
        self.event_handler = event_handler

    async def __call__(self, command: CreateDiaryCardCommand) -> None:
        user_id: UUID = self.id_provider.get_current_user_id()
        command.user_id = user_id
        diary_card: DiaryCardDM = DiaryCardDM.create(command)
        await self.db_gateway.create(diary_card)
        await self.event_handler(diary_card.pull_events()[0])
        await self.uow.commit()
        return None
