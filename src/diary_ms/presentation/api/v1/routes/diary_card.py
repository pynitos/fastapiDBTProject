from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO, NewDiaryCardDTO
from src.diary_ms.application.dto.pagination import Pagination
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.presentation.api.deps import GetOwnDiaryCardsDep, GetDiaryCardDep, CreateDiaryCardDep

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


@router.get('/<id:UUID>', response_model=DiaryCardDM)
async def get_diary_card_by_id(
        id: UUID,
        interactor: GetDiaryCardDep,
) -> list[DiaryCardDM]:
    diary_card = interactor(id)
    return diary_card


@router.post('/', response_model=list[DiaryCardDM])
async def create_diary_card(

        interactor: CreateDiaryCardDep,
) -> list[DiaryCardDM]:
    interactor(
        NewDiaryCardDTO(
            pagination=Pagination(limit=limit, offset=offset)
        )
    )
    return diary_card
