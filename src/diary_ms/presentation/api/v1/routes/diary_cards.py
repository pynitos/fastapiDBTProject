from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardDTO,
    GetOwnDiaryCardsDTO,
    OwnDiaryCardDTO,
)
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    DiaryCardForUpdateDTO,
)
from src.diary_ms.application.diary_card.interactors.queries.get_diary_card_for_update import GetDiaryCardForUpdate
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.presentation.api.deps import MediatorDep
from src.diary_ms.presentation.api.v1.routes.schemas.diary_card import (
    CreateDiaryCardReq,
    UpdateDiaryCardReq,
)

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[OwnDiaryCardDTO])
async def get_diary_cards(
    mediator: MediatorDep,
    limit: int = 10,
    offset: int = 0,
) -> list[OwnDiaryCardDTO]:
    diary_cards = await mediator.handle_query(GetOwnDiaryCardsDTO(pagination=Pagination(limit=limit, offset=offset)))
    return diary_cards


@router.get("/<id:UUID>", response_model=OwnDiaryCardDTO)
async def get_own_diary_card_by_id(
    id: UUID,
    mediator: MediatorDep,
) -> OwnDiaryCardDTO:
    diary_card: OwnDiaryCardDTO | None = await mediator.handle_query(GetOwnDiaryCardDTO(id))
    if not diary_card:
        raise HTTPException(404, f"Diary card with id: {id} not found.")
    return diary_card


@router.get("/upd/<id:UUID>", response_model=DiaryCardForUpdateDTO)
async def get_diary_card_for_update(
    id: UUID,
    mediator: MediatorDep,
) -> DiaryCardForUpdateDTO:
    diary_card: DiaryCardForUpdateDTO | None = await mediator.handle_query(GetDiaryCardForUpdate(id))
    if not diary_card:
        raise HTTPException(404, f"Diary card with id: {id} not found.")
    return diary_card


@router.post("/", status_code=201, response_model=None)
async def create_diary_card(
    schema: CreateDiaryCardReq,
    mediator: MediatorDep,
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
    result = await mediator.handle_command(command)
    return result


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_diary_card(
    id: UUID,
    schema: UpdateDiaryCardReq,
    mediator: MediatorDep,
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
    return await mediator.handle_command(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def delete_diary_card(
    id: UUID,
    mediator: MediatorDep,
) -> None:
    await mediator.handle_command(DeleteDiaryCardCommand(id=id))
