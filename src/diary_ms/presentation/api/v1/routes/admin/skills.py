from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from src.diary_ms.application.admin.skill.dto.skill import (
    GetSkillAdminDTO,
    GetSkillsAdminDTO,
    SkillAdminDTO,
    SkillsAdminFilters,
)
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.commands.skill.create_skill import CreateSkillAdminCommand
from src.diary_ms.domain.model.commands.skill.delete_skill import DeleteSkillAdminCommand
from src.diary_ms.domain.model.commands.skill.update_skill import UpdateSkillAdminCommand
from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.routes.admin.schemas.skill import CreateSkillAdminReq, UpdateSkillAdminReq

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[SkillAdminDTO])
async def admin_get_skills(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
    type: SkillType | None = SkillType.DBT,
) -> list[SkillAdminDTO]:
    skills: list[SkillAdminDTO] = await sender.send_query(
        GetSkillsAdminDTO(pagination=Pagination(limit=limit, offset=offset), filters=SkillsAdminFilters(type=type))
    )
    return skills


@router.get("/<id:UUID>", response_model=SkillAdminDTO)
async def admin_get_skill_by_id(
    id: UUID,
    sender: SenderDep,
) -> SkillAdminDTO:
    skill: SkillAdminDTO | None = await sender.send_query(GetSkillAdminDTO(id))
    if not skill:
        raise HTTPException(404, f"Skill with id: {id} not found.")
    return skill


@router.post("/", status_code=201, response_model=None)
async def admin_create_skill(
    schema: CreateSkillAdminReq,
    sender: SenderDep,
) -> None:
    command = CreateSkillAdminCommand(
        name=schema.name,
        category=schema.category,
        group=schema.group,
        type=schema.type,
        description=schema.description,
    )
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def admin_update_skill(
    id: UUID,
    schema: UpdateSkillAdminReq,
    sender: SenderDep,
) -> None:
    command = UpdateSkillAdminCommand(
        id=id,
        name=schema.name,
        category=schema.category,
        group=schema.group,
        type=schema.type,
        description=schema.description,
    )
    return await sender.send_command(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def admin_delete_skill(
    id: UUID,
    sender: SenderDep,
) -> None:
    await sender.send_command(DeleteSkillAdminCommand(id))
