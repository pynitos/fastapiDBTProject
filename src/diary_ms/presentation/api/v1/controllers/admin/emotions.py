from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from src.diary_ms.application.admin.emotion.dto.emotion import (
    EmotionAdminDTO,
    GetEmotionAdminDTO,
    GetEmotionsAdminDTO,
)
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.diary_card.dto.commands.emotion.create_emotion import CreateEmotionAdminCommand
from src.diary_ms.application.diary_card.dto.commands.emotion.delete_emotion import DeleteEmotionAdminCommand
from src.diary_ms.application.diary_card.dto.commands.emotion.update_emotion import UpdateEmotionAdminCommand
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.controllers.admin.schemas.emotion import (
    CreateEmotionAdminReq,
    UpdateEmotionAdminReq,
)

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[EmotionAdminDTO])
async def admin_get_emotions(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[EmotionAdminDTO]:
    emotions: list[EmotionAdminDTO] = await sender.send_query(
        GetEmotionsAdminDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return emotions


@router.get("/<id:UUID>", response_model=EmotionAdminDTO)
async def admin_get_emotion_by_id(
    id: UUID,
    sender: SenderDep,
) -> EmotionAdminDTO:
    emotion: EmotionAdminDTO = await sender.send_query(GetEmotionAdminDTO(id))
    if not emotion:
        raise HTTPException(404, f"Emotion with id: {id} not found.")
    return emotion


@router.post("/", status_code=201, response_model=None)
async def admin_create_emotion(
    schema: CreateEmotionAdminReq,
    sender: SenderDep,
) -> None:
    command = CreateEmotionAdminCommand(name=schema.name, description=schema.description)
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def admin_update_emotion(
    id: UUID,
    schema: UpdateEmotionAdminReq,
    sender: SenderDep,
) -> None:
    command = UpdateEmotionAdminCommand(
        id=id,
        name=schema.name,
        description=schema.description,
    )
    await sender.send_command(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def admin_delete_emotion(
    id: UUID,
    sender: SenderDep,
) -> None:
    await sender.send_command(DeleteEmotionAdminCommand(id))
