from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager

from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class CreateDiaryCardState(StatesGroup):
    preview = State()
    mood = State()
    description = State()
    date_of_entry = State()
    targets = State()
    emotions = State()
    medicaments = State()
    skills = State()
    CONFIRMATION = State()


class GetOwnDiaryCardsState(StatesGroup):
    view = State()


async def start_create_diary_card(
    dialog_manager: DialogManager,
    wishlist_id: DiaryCardId,
):
    await dialog_manager.start(
        CreateDiaryCardState.mood,
        data={"wishlist_id": wishlist_id.value},
    )


async def start_get_diary_cards(
    dialog_manager: DialogManager,
):
    await dialog_manager.start(
        GetOwnDiaryCardsState.view,
    )
