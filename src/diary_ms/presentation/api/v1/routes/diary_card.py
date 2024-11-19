from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from src.diary_ms.application.dto.pagination import Pagination
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.commands.create_skill import CreateSkillCommand
from src.diary_ms.domain.model.commands.create_target import CreateTargetCommand
from src.diary_ms.presentation.api.deps import GetOwnDiaryCardsDep, GetDiaryCardDep, CreateDiaryCardDep
from src.diary_ms.presentation.api.v1.routes.schemas.diary_card import CreateDiaryCardReq

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
) -> list[DiaryCardDM]:
    diary_card = await interactor(id)
    return diary_card


@router.post('/', status_code=201, response_model=None)
async def create_diary_card(
        schema: CreateDiaryCardReq,
        interactor: CreateDiaryCardDep, # type: ignore
) -> None:
    command = CreateDiaryCardCommand(
        mood=schema.mood,
        description=schema.description,
        date_of_entry=schema.date_of_entry,
        targets=[CreateTargetCommand(
            urge=x.urge, action=x.action
        ) for x in schema.targets if schema.targets],
        emotions=[CreateEmotionCommand(
            name=x.name,
            description=x.description
        ) for x in schema.emotions if schema.emotions],
        medicaments=[CreateMedicamentCommand(
            name=x.name, dosage=x.dosage,
        ) for x in schema.medicaments if schema.medicaments],
        skills=[CreateSkillCommand(
            category=x.category,
            group=x.group,
            name=x.name,
            type=x.type,
        ) for x in schema.skills if schema.skills],
    )
    return await interactor(command)
