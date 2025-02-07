from http import HTTPStatus

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.diary_card.dto.emotion import EmotionDTO, GetEmotionsDTO
from src.diary_ms.presentation.api.deps import SenderDep

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[EmotionDTO])
async def get_emotions(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[EmotionDTO]:
    emotions: list[EmotionDTO] = await sender.send_query(
        GetEmotionsDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return emotions
