from src.diary_ms.application.common.interfaces.mediator.base import Mediator
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardDTO,
    GetOwnDiaryCardsDTO,
)
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    GetDiaryCardForUpdateDTO,
)
from src.diary_ms.application.diary_card.interactors.commands.create_diary_card import (
    CreateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.delete_diary_card import (
    DeleteDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.update_diary_card import (
    UpdateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.events.diary_card_created import (
    DiaryCardCreatedEventHandler,
)
from src.diary_ms.application.diary_card.interactors.queries.get_diary_card_for_update import (
    GetDiaryCardForUpdate,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_card import (
    GetOwnDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_cards import (
    GetOwnDiaryCards,
)
from src.diary_ms.application.mediator import MediatorImpl
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent


def init_mediator(
    create_dc: CreateDiaryCard,
    update_dc: UpdateDiaryCard,
    delete_dc: DeleteDiaryCard,
    get_dcs: GetOwnDiaryCards,
    get_dc: GetOwnDiaryCard,
    get_dc_for_upd: GetDiaryCardForUpdate,
    dc_created: DiaryCardCreatedEventHandler,
) -> Mediator:
    mediator = MediatorImpl()

    mediator.register_event_handler(DiaryCardCreatedEvent, dc_created)

    mediator.register_command_handler(CreateDiaryCardCommand, create_dc)
    mediator.register_command_handler(UpdateDiaryCardCommand, update_dc)
    mediator.register_command_handler(DeleteDiaryCardCommand, delete_dc)

    mediator.register_query_handler(GetOwnDiaryCardDTO, get_dc)
    mediator.register_query_handler(GetOwnDiaryCardsDTO, get_dcs)
    mediator.register_query_handler(GetDiaryCardForUpdateDTO, get_dc_for_upd)

    return mediator
