from dataclasses import dataclass, asdict

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.diary_ms.api.deps import GetOwnDiaryCardsDep
from app.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from app.diary_ms.application.dto.pagination import Pagination
from app.diary_ms.domain.models.diary_card import DiaryCardDM

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


@dataclass
class DCDM:
    user_id: str
    description: str

@dataclass
class DCOUT:
    ds: list[DCDM]


@router.get('/s', response_model=DCOUT)
async def get_diary_cards(
        interactor: GetOwnDiaryCardsDep,
        limit: int = 10,
        offset: int = 0,
) -> DCOUT:

    return DCOUT([DCDM(user_id='sd', description='sd2')])