from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.presentation.api.deps import GetOwnDiaryCardsDep
from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from src.diary_ms.application.dto.pagination import Pagination
from src.diary_ms.domain.model.entities import DiaryCardDM

router = APIRouter(route_class=DishkaRoute)


@router.get('/', response_model=list[DiaryCardDM])
async def get_diary_cards(
        interactor: GetOwnDiaryCardsDep,
        limit: int = 10,
        offset: int = 0,
) -> list[DiaryCardDM]:
    diary_cards = interactor(
        GetOwnDiaryCardsDTO(
            pagination=Pagination(limit=limit, offset=offset)
        )
    )
    return diary_cards
