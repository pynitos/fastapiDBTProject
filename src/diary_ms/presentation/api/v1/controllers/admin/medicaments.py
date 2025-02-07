from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.diary_ms.application.admin.medicament.dto.medicament import (
    GetMedicamentAdminDTO,
    GetMedicamentsAdminDTO,
    MedicamentAdminDTO,
)
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.commands.medicament.create_medicament import (
    CreateMedicamentAdminCommand,
)
from src.diary_ms.domain.model.commands.medicament.delete_medicament import (
    DeleteMedicamentAdminCommand,
)
from src.diary_ms.domain.model.commands.medicament.update_medicament import (
    UpdateMedicamentAdminCommand,
)
from src.diary_ms.presentation.api.deps import SenderDep
from src.diary_ms.presentation.api.v1.controllers.admin.schemas.medicament import (
    CreateMedicamentAdminReq,
    UpdateMedicamentAdminReq,
)

router = APIRouter(
    route_class=DishkaRoute,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            HTTPStatus.UNAUTHORIZED.phrase: HTTPStatus.UNAUTHORIZED.description,
        }
    },
)


@router.get("/", response_model=list[MedicamentAdminDTO])
async def get_medicaments(
    sender: SenderDep,
    limit: int = 10,
    offset: int = 0,
) -> list[MedicamentAdminDTO]:
    medicaments: list[MedicamentAdminDTO] = await sender.send_query(
        GetMedicamentsAdminDTO(pagination=Pagination(limit=limit, offset=offset))
    )
    return medicaments


@router.get("/<id:UUID>", response_model=MedicamentAdminDTO)
async def get_medicament_by_id(
    id: UUID,
    sender: SenderDep,
) -> MedicamentAdminDTO:
    medicament: MedicamentAdminDTO = await sender.send_query(GetMedicamentAdminDTO(id))
    return medicament


@router.post("/", status_code=201, response_model=None)
async def create_medicament(
    schema: CreateMedicamentAdminReq,
    sender: SenderDep,
) -> None:
    command = CreateMedicamentAdminCommand(
        name=schema.name,
        dosage=schema.dosage,
    )
    await sender.send_command(command)


@router.patch("/<id:UUID>", status_code=HTTPStatus.NO_CONTENT, response_model=None)
async def update_medicament(
    id: UUID,
    schema: UpdateMedicamentAdminReq,
    sender: SenderDep,
) -> None:
    command = UpdateMedicamentAdminCommand(
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
    await sender.send_command(DeleteMedicamentAdminCommand(id=id))
