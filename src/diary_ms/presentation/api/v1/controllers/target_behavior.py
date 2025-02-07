from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnTargetDTO,
    GetOwnTargetsDTO,
    OwnTargetDTO,
)
from src.diary_ms.domain.model.commands.target_behavior.create_target import CreateTargetCommand
from src.diary_ms.domain.model.commands.target_behavior.delete_target import DeleteTargetCommand
from src.diary_ms.domain.model.commands.target_behavior.update_target import UpdateTargetCommand
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.controllers.schemas.target_behavior import (
    CreateOwnTargetReq,
    UpdateOwnTargetReq,
)

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[OwnTargetDTO])
async def get_targets(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[OwnTargetDTO]:
    targets = await sender.send_query(GetOwnTargetsDTO(pagination=Pagination(limit=limit, offset=offset)))
    return targets


@router.get("/<id:UUID>", response_model=OwnTargetDTO)
async def get_own_target_by_id(
    id: UUID,
    sender: SenderDep,
) -> OwnTargetDTO:
    target: OwnTargetDTO = await sender.send_query(GetOwnTargetDTO(id))
    return target


@router.post("/", status_code=201, response_model=None)
async def create_target(
    schema: CreateOwnTargetReq,
    sender: SenderDep,
) -> None:
    command = CreateTargetCommand(
        urge=schema.urge,
        action=schema.action
    )
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_target(
    id: UUID,
    schema: UpdateOwnTargetReq,
    sender: SenderDep,
) -> None:
    command = UpdateTargetCommand(
        id=id,
        urge=schema.urge,
        action=schema.action,
    )
    await sender.send_command(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def delete_target(
    id: UUID,
    sender: SenderDep,
) -> None:
    await sender.send_command(DeleteTargetCommand(id=id))
