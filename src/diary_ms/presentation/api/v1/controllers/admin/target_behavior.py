from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.admin.target_behavior.dto.target_behavior import (
    GetTargetAdminDTO,
    GetTargetsAdminDTO,
    TargetAdminDTO,
)
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.commands.target_behavior.create_target import (
    CreateTargetAdminCommand,
)
from src.diary_ms.domain.model.commands.target_behavior.delete_target import (
    DeleteTargetAdminCommand,
)
from src.diary_ms.domain.model.commands.target_behavior.update_target import (
    UpdateTargetAdminCommand,
)
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.controllers.admin.schemas.target_behavior import (
    CreateTargetAdminReq,
    UpdateTargetAdminReq,
)

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: HTTPStatus.UNAUTHORIZED.description,
        }
    },
)


@router.get("/", response_model=list[TargetAdminDTO])
async def get_targets(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[TargetAdminDTO]:
    targets: list[TargetAdminDTO] = await sender.send_query(
        GetTargetsAdminDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return targets


@router.get("/<id:UUID>", response_model=TargetAdminDTO)
async def get_target_by_id(
    id: UUID,
    sender: SenderDep,
) -> TargetAdminDTO:
    target: TargetAdminDTO = await sender.send_query(GetTargetAdminDTO(id))
    return target


@router.post("/", status_code=201, response_model=None)
async def create_target(
    schema: CreateTargetAdminReq,
    sender: SenderDep,
) -> None:
    command = CreateTargetAdminCommand(urge=schema.urge, action=schema.action)
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_target(
    id: UUID,
    schema: UpdateTargetAdminReq,
    sender: SenderDep,
) -> None:
    command = UpdateTargetAdminCommand(
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
    await sender.send_command(DeleteTargetAdminCommand(id=id))
