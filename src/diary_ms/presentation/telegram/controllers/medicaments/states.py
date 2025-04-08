from uuid import UUID

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager


class CreateMedicamentSG(StatesGroup):
    name = State()
    dosage = State()
    preview = State()


class UpdateMedicamentSG(StatesGroup):
    name = State()
    dosage = State()
    preview = State()


class GetOwnMedicamentsSG(StatesGroup):
    view = State()


class GetOwnMedicamentSG(StatesGroup):
    view = State()
    confirm_delete = State()


async def start_create_medicament(
    dialog_manager: DialogManager,
):
    await dialog_manager.start(
        CreateMedicamentSG.name,
    )


async def start_update_medicament(
    dialog_manager: DialogManager,
    medicament_id: UUID,
):
    await dialog_manager.start(
        UpdateMedicamentSG.name,
        data={"medicament_id": medicament_id},
    )


async def start_view_medicament(
    dialog_manager: DialogManager,
    medicament_id: UUID,
):
    await dialog_manager.start(
        GetOwnMedicamentSG.view,
        data={
            "medicament_id": medicament_id,
        },
    )
