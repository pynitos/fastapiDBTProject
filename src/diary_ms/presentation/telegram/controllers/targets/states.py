from uuid import UUID

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager


class GetTargetsSG(StatesGroup):
    view = State()


class ViewTargetSG(StatesGroup):
    view = State()
    confirm_delete = State()


class CreateTargetSG(StatesGroup):
    urge = State()
    action = State()
    confirm = State()


class UpdateTargetSG(StatesGroup):
    urge = State()
    action = State()
    confirm = State()


class DeleteTargetSG(StatesGroup):
    confirm = State()


async def start_view_target(
    dialog_manager: DialogManager,
    target_id: UUID,
):
    await dialog_manager.start(
        ViewTargetSG.view,
        data={
            "target_id": target_id,
        },
    )


async def start_update_target(
    dialog_manager: DialogManager,
    target_id: UUID,
):
    await dialog_manager.start(
        UpdateTargetSG.urge,
        data={
            "target_id": target_id,
        },
    )
