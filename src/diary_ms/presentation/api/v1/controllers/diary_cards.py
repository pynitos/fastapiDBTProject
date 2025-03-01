import logging
from http import HTTPStatus
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.interfaces.task_sender import TaskSender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.application.diary_card.dto.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardDTO,
    GetOwnDiaryCardsDTO,
    OwnDiaryCardDTO,
)
from src.diary_ms.application.diary_card.interactors.commands.create_diary_cards_report import (
    CreateDiaryCardsReportCommand,
    CreateDiaryCardsReportDTO,
)
from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.controllers.schemas.diary_card import (
    CreateDiaryCardReq,
    UpdateDiaryCardReq,
)

logger = logging.getLogger(__name__)

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
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[OwnDiaryCardDTO] | dict:
    diary_cards = await sender.send_query(GetOwnDiaryCardsDTO(pagination=Pagination(limit=limit, offset=offset)))
    return diary_cards


@router.get("/<id:UUID>", response_model=OwnDiaryCardDTO)
async def get_own_diary_card_by_id(
    id: UUID,
    sender: SenderDep,
) -> OwnDiaryCardDTO:
    diary_card: OwnDiaryCardDTO = await sender.send_query(GetOwnDiaryCardDTO(id))
    return diary_card


@router.get("/data", response_model=DataForDiaryCardDTO)
async def get_data_for_create_or_update_diary_card(
    sender: SenderDep, skill_type: SkillType = SkillType.DBT
) -> DataForDiaryCardDTO:
    diary_card: DataForDiaryCardDTO = await sender.send_query(GetDataForDiaryCardQuery(skill_type))
    return diary_card


@router.post("/", status_code=201, response_model=None)
async def create_diary_card(
    schema: CreateDiaryCardReq,
    sender: SenderDep,
) -> None:
    skills: list[CreateDiaryCardCommand.Skill] | None = (
        [CreateDiaryCardCommand.Skill(id=s.id, situation=s.situation) for s in schema.skills] if schema.skills else None
    )
    command = CreateDiaryCardCommand(
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=schema.targets,
        emotions=schema.emotions,
        medicaments=schema.medicaments,
        skills=skills,
        skills_type=schema.type,
    )
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_diary_card(
    id: UUID,
    schema: UpdateDiaryCardReq,
    sender: SenderDep,
) -> None:
    skills = [UpdateDiaryCardCommand.Skill(s.id, s.situation) for s in schema.skills] if schema.skills else None
    command = UpdateDiaryCardCommand(
        id=id,
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=schema.targets,
        emotions=schema.emotions,
        medicaments=schema.medicaments,
        skills=skills,
    )
    await sender.send_command(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def delete_diary_card(
    id: UUID,
    sender: SenderDep,
) -> None:
    await sender.send_command(DeleteDiaryCardCommand(id=id))


@router.post("/report", status_code=200, response_model=CreateDiaryCardsReportDTO)
async def create_diary_cards_report(sender: SenderDep) -> CreateDiaryCardsReportDTO:
    return await sender.send_command(CreateDiaryCardsReportCommand())


@router.get("/report", status_code=200, response_model=str)
async def get_diary_cards_report(task_id: str, sender: FromDishka[TaskSender]) -> str:
    return await sender.get_result(task_id)
