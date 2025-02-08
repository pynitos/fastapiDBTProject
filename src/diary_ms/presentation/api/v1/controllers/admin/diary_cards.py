from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.admin.diary_card.dto.diary_card import (
    DiaryCardAdminDTO,
    GetDiaryCardAdminDTO,
    GetDiaryCardsAdminDTO,
)
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardAdminCommand
from src.diary_ms.presentation.api.deps import SenderDep

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[DiaryCardAdminDTO])
async def get_diary_cards(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[DiaryCardAdminDTO]:
    diary_cards: list[DiaryCardAdminDTO] = await sender.send_query(
        GetDiaryCardsAdminDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return diary_cards


@router.get("/<id:UUID>", response_model=DiaryCardAdminDTO)
async def get_diary_card_by_id(
    id: UUID,
    sender: SenderDep,
) -> DiaryCardAdminDTO:
    diary_card: DiaryCardAdminDTO = await sender.send_query(GetDiaryCardAdminDTO(id))
    return diary_card


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def delete_diary_card(
    id: UUID,
    sender: SenderDep,
) -> None:
    await sender.send_command(DeleteDiaryCardAdminCommand(id=id))
