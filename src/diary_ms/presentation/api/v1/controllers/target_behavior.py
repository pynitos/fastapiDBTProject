from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from diary_ms.application.common.dto.pagination import Pagination
from diary_ms.application.target_behavior.dto.commands.create_target import CreateTargetCommand
from diary_ms.application.target_behavior.dto.commands.delete_target import DeleteTargetCommand
from diary_ms.application.target_behavior.dto.commands.update_target import UpdateTargetCommand
from diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnAndDefaultTargetsQuery,
    GetOwnTargetQuery,
    OwnTargetResultDTO,
    OwnTargetsResultDTO,
)
from diary_ms.presentation.api.deps import SenderDep
from diary_ms.presentation.api.v1.controllers.schemas.target_behavior import (
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


@router.get("/", response_model=OwnTargetsResultDTO)
async def get_targets(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> OwnTargetsResultDTO:
    targets: OwnTargetsResultDTO = await sender.send_query(
        GetOwnAndDefaultTargetsQuery(pagination=Pagination(limit=limit, offset=offset))
    )
    return targets


@router.get("/<id:UUID>", response_model=OwnTargetResultDTO)
async def get_own_target_by_id(
    id: UUID,
    sender: SenderDep,
) -> OwnTargetResultDTO:
    target: OwnTargetResultDTO = await sender.send_query(GetOwnTargetQuery(id))
    return target


@router.post("/", status_code=201, response_model=None)
async def create_target(
    schema: CreateOwnTargetReq,
    sender: SenderDep,
) -> None:
    command = CreateTargetCommand(urge=schema.urge, action=schema.action)
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_target(
    id: UUID,
    schema: UpdateOwnTargetReq,
    sender: SenderDep,
) -> None:
    command = UpdateTargetCommand(
        target_id=id,
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
