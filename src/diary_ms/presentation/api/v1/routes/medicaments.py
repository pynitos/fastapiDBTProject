from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.medicament.dto.medicament import (
    GetOwnMedicamentDTO,
    GetOwnMedicamentsDTO,
    OwnMedicamentDTO,
)
from src.diary_ms.domain.model.commands.medicament.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.commands.medicament.delete_medicament import DeleteMedicamentCommand
from src.diary_ms.domain.model.commands.medicament.update_medicament import UpdateMedicamentCommand
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.routes.schemas.medicament import CreateOwnMedicamentReq, UpdateOwnMedicamentReq

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: "No permission.",
        }
    },
)


@router.get("/", response_model=list[OwnMedicamentDTO])
async def get_medicaments(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[OwnMedicamentDTO]:
    medicaments: list[OwnMedicamentDTO] = await sender.send_query(
        GetOwnMedicamentsDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return medicaments


@router.get("/<id:UUID>", response_model=OwnMedicamentDTO)
async def get_own_medicament_by_id(
    id: UUID,
    sender: SenderDep,
) -> OwnMedicamentDTO:
    medicament: OwnMedicamentDTO = await sender.send_query(GetOwnMedicamentDTO(id))
    if not medicament:
        raise HTTPException(404, f"Medicament with id: {id} not found.")
    return medicament


@router.post("/", status_code=201, response_model=None)
async def create_medicament(
    schema: CreateOwnMedicamentReq,
    sender: SenderDep,
) -> None:
    command = CreateMedicamentCommand(
        name=schema.name,
        dosage=schema.dosage,
    )
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_medicament(
    id: UUID,
    schema: UpdateOwnMedicamentReq,
    sender: SenderDep,
) -> None:
    command = UpdateMedicamentCommand(
        id=id,
        name=schema.name,
        dosage=schema.dosage,
    )
    await sender.send_command(command)


@router.delete("/<id:UUID>", status_code=204, response_model=None)
async def delete_medicament(
    id: UUID,
    sender: SenderDep,
) -> None:
    await sender.send_command(DeleteMedicamentCommand(id=id))
