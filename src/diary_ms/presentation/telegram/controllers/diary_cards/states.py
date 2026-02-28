from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager

from diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class CreateDiaryCardSG(StatesGroup):
    mood = State()
    description = State()
    date_of_entry = State()
    targets = State()
    target_intensity = State()
    target_action = State()
    target_effectiveness = State()
    emotions = State()
    medicaments = State()
    skills = State()
    skill_effectiveness = State()
    skill_usage = State()
    CONFIRMATION = State()


class GetOwnDiaryCardsSG(StatesGroup):
    view = State()
    detail_view = State()
    confirm_delete = State()


async def start_create_diary_card(
    dialog_manager: DialogManager,
    wishlist_id: DiaryCardId,
) -> None:
    await dialog_manager.start(
        CreateDiaryCardSG.mood,
        data={"wishlist_id": wishlist_id.value},
    )


async def start_get_diary_cards(
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        GetOwnDiaryCardsSG.view,
    )
