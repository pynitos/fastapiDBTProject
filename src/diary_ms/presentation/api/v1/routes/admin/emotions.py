from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.admin.emotion.dto.emotion import (
    EmotionAdminDTO,
    GetEmotionsAdminDTO,
)
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionAdminCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.presentation.api.deps import (
    MediatorDep,
    UpdateDiaryCardDep,
)
from src.diary_ms.presentation.api.v1.routes.admin.schemas.emotion import (
    CreateEmotionAdminReq,
)
from src.diary_ms.presentation.api.v1.routes.schemas.diary_card import (
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


@router.get("/", response_model=list[EmotionAdminDTO])
async def admin_get_emotions(
    mediator: MediatorDep,
    limit: int = 10,
    offset: int = 0,
) -> list[EmotionAdminDTO]:
    emotions: list[EmotionAdminDTO] = await mediator.handle_query(
        GetEmotionsAdminDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return emotions


# @router.get("/<id:UUID>", response_model=OwnDiaryCardDTO)
# async def admin_get_emotion_by_id(
#     id: UUID,
#     mediator: MediatorDep,
# ) -> EmotionAdminDTO:
#     emotion: EmotionDTO | None = await mediator(id)
#     if not emotion:
#         raise HTTPException(404, f"Diary card with id: {id} not found.")
#     return emotion


# @router.get("/upd/<id:UUID>", response_model=DiaryCardForUpdateDTO)
# async def admin_get_emotion_for_update(
#     id: UUID,
#     interactor: GetDiaryCardForUpdateDep,
# ) -> DiaryCardForUpdateDTO:
#     diary_card: DiaryCardForUpdateDTO | None = await interactor(id)
#     if not diary_card:
#         raise HTTPException(404, f"Emotion with id: {id} not found.")
#     return diary_card


@router.post("/", status_code=201, response_model=None)
async def admin_create_emotion(
    schema: CreateEmotionAdminReq,
    mediator: MediatorDep,
) -> None:
    command = CreateEmotionAdminCommand(
        name=schema.name, description=schema.description
    )
    await mediator.handle_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def admin_update_emotion(
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


# @router.delete("/<id:UUID>", status_code=204, response_model=None)
# async def admin_delete_emotion(
#     id: UUID,
#     interactor: DeleteDiaryCardDep,
# ) -> None:
#     await interactor(DeleteDiaryCardCommand(id=id))
