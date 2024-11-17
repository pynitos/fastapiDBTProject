from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from src.diary_ms.application.dto.pagination import Pagination
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.presentation.api.deps import GetOwnDiaryCardsDep, GetDiaryCardDep, CreateDiaryCardDep

router = APIRouter(route_class=DishkaRoute)


@router.get('/', response_model=list[DiaryCardDM])
async def get_diary_cards(
        interactor: GetOwnDiaryCardsDep,
        limit: int = 10,
        offset: int = 0,
) -> list[DiaryCardDM]:
    diary_cards = await interactor(
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
    diary_card = await interactor(id)
    return diary_card


@router.post('/', status_code=201, response_model=DiaryCardId)
async def create_diary_card(
        command: CreateDiaryCardCommand,
        interactor: CreateDiaryCardDep,
) -> DiaryCardId:
    new_diary_card_id = await interactor(command)
    return new_diary_card_id
