from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from http import HTTPStatus
from fastapi import APIRouter, HTTPException

from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from src.diary_ms.application.dto.pagination import Pagination
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.commands.create_skill import CreateSkillCommand
from src.diary_ms.domain.model.commands.create_target import CreateTargetCommand
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.presentation.api.deps import GetOwnDiaryCardsDep, GetDiaryCardDep, CreateDiaryCardDep, UpdateDiaryCardDep, DeleteDiaryCardDep
from src.diary_ms.presentation.api.v1.routes.schemas.diary_card import CreateDiaryCardReq, UpdateDiaryCardReq

router = APIRouter(route_class=DishkaRoute)


@router.get('/', response_model=list[DiaryCardDM])
async def get_diary_cards(
        interactor: GetOwnDiaryCardsDep, # type: ignore
        limit: int = 10,
        offset: int = 0,
) -> list[DiaryCardDM]:
    diary_cards = await interactor(
        GetOwnDiaryCardsDTO(
            pagination=Pagination(limit=limit, offset=offset)
        )
    )
    return diary_cards


@router.get('/<id:UUID>', response_model=DiaryCardDM)
async def get_diary_card_by_id(
        id: UUID,
        interactor: GetDiaryCardDep, # type: ignore
) -> DiaryCardDM:
    diary_card: DiaryCardDM | None = await interactor(id)
    if not diary_card:
        raise HTTPException(404, f'Diary card with id: {id} not found.')
    return diary_card


@router.post('/', status_code=201, response_model=None)
async def create_diary_card(
        schema: CreateDiaryCardReq,
        interactor: CreateDiaryCardDep,
) -> None:
    command = CreateDiaryCardCommand(
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=[CreateTargetCommand(
            urge=x.urge, action=x.action
        ) for x in schema.targets]
        if schema.targets else None,
        emotions=[CreateEmotionCommand(
            name=x.name,
            description=x.description
        ) for x in schema.emotions]
        if schema.emotions else None,
        medicaments=[CreateMedicamentCommand(
            name=x.name, dosage=x.dosage,
        ) for x in schema.medicaments]
        if schema.medicaments else None,
        skills=[CreateSkillCommand(
            category=x.category,
            group=x.group,
            name=x.name,
            type=x.type,
        ) for x in schema.skills]
        if schema.skills else None,
    )
    return await interactor(command)


@router.patch('/<id:UUID>', status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_diary_card(
        id: UUID,
        schema: UpdateDiaryCardReq,
        interactor: UpdateDiaryCardDep,
) -> None:
    command = UpdateDiaryCardCommand(
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=[CreateTargetCommand(
            urge=x.urge, action=x.action
        ) for x in schema.targets]
        if schema.targets else None,
        emotions=[CreateEmotionCommand(
            name=x.name,
            description=x.description
        ) for x in schema.emotions]
        if schema.emotions else None,
        medicaments=[CreateMedicamentCommand(
            name=x.name, dosage=x.dosage,
        ) for x in schema.medicaments]
        if schema.medicaments else None,
        skills=[CreateSkillCommand(
            category=x.category,
            group=x.group,
            name=x.name,
            type=x.type,
        ) for x in schema.skills]
        if schema.skills else None,
    )
    return await interactor(command)


@router.delete('/<id:UUID>', status_code=204, response_model=None)
async def delete_diary_card(
        id: UUID,
        interactor: DeleteDiaryCardDep,
) -> None:
    await interactor(DeleteDiaryCardCommand(id=DiaryCardId(id)))



