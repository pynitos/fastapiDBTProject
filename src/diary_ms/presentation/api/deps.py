from dishka import FromDishka

from src.diary_ms.application.diary_card.interactors.commands.create_diary_card import (
    CreateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.delete_diary_card import (
    DeleteDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.update_diary_card import (
    UpdateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.queries.get_diary_card_for_update import (
    GetDiaryCardForUpdate,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_card import (
    GetOwnDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_cards import (  # noqa: E501
    GetOwnDiaryCards,
)

GetOwnDiaryCardsDep = FromDishka[GetOwnDiaryCards]
GetDiaryCardDep = FromDishka[GetOwnDiaryCard]
CreateDiaryCardDep = FromDishka[CreateDiaryCard]
UpdateDiaryCardDep = FromDishka[UpdateDiaryCard]
DeleteDiaryCardDep = FromDishka[DeleteDiaryCard]
GetDiaryCardForUpdateDep = FromDishka[GetDiaryCardForUpdate]
