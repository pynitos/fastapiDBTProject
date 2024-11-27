from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO, OwnDiaryCardDTO
from src.diary_ms.application.dto.for_update_diary_card import DiaryCardForUpdateDTO
from src.diary_ms.application.dto.pagination import Pagination
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM, DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.presentation.api.deps import (
    CreateDiaryCardDep,
    DeleteDiaryCardDep,
    GetDiaryCardDep,
    GetDiaryCardForUpdateDep,
    GetOwnDiaryCardsDep,
    UpdateDiaryCardDep,
)
from src.diary_ms.presentation.api.v1.routes.schemas.diary_card import (
    CreateDiaryCardReq,
    UpdateDiaryCardReq,
)

router = APIRouter(route_class=DishkaRoute)


@router.get("/", response_model=list[OwnDiaryCardDTO])
async def get_diary_cards(
    interactor: GetOwnDiaryCardsDep,
    limit: int = 10,
    offset: int = 0,
) -> list[OwnDiaryCardDTO]:
    diary_cards = await interactor(
        GetOwnDiaryCardsDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return diary_cards


@router.get("/<id:UUID>", response_model=OwnDiaryCardDTO)
async def get_own_diary_card_by_id(
    id: UUID,
    interactor: GetDiaryCardDep,
) -> DiaryCardDM:
    diary_card: OwnDiaryCardDTO | None = await interactor(id)
    if not diary_card:
        raise HTTPException(404, f"Diary card with id: {id} not found.")
    return diary_card


@router.get("/upd/<id:UUID>", response_model=DiaryCardForUpdateDTO)
async def get_diary_card_for_update(
    id: UUID,
    interactor: GetDiaryCardForUpdateDep,
) -> DiaryCardForUpdateDTO:
    diary_card: DiaryCardForUpdateDTO | None = await interactor(id)
    if not diary_card:
        raise HTTPException(404, f"Diary card with id: {id} not found.")
    return diary_card


@router.post("/", status_code=201, response_model=None)
async def create_diary_card(
    schema: CreateDiaryCardReq,
    interactor: CreateDiaryCardDep,
) -> None:
    command = CreateDiaryCardCommand(
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=schema.targets,
        emotions=schema.emotions,
        medicaments=schema.medicaments,
        skills=schema.skills,
        type=schema.type,
    )
    return await interactor(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_diary_card(
    id: UUID,
    schema: UpdateDiaryCardReq,
    interactor: UpdateDiaryCardDep,
) -> None:
    command = UpdateDiaryCardCommand(
        id=id,
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=schema.targets,
        emotions=schema.emotions,
        medicaments=schema.medicaments,
        skills=schema.skills,
    )
    return await interactor(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def delete_diary_card(
    id: UUID,
    interactor: DeleteDiaryCardDep,
) -> None:
    await interactor(DeleteDiaryCardCommand(id=DiaryCardId(id)))
