from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.dto.pagination import PAGE_SIZE, Pagination
from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.medicament.dto.commands.delete_medicament import DeleteMedicamentCommand
from src.diary_ms.application.medicament.dto.medicament import (
    GetOwnMedicamentDTO,
    GetOwnMedicamentsDTO,
    OwnMedicamentDTO,
)
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.presentation.telegram.common.constants import (
    ADD_BTN_TXT,
    BACK_BTN_TXT,
    BACK_TO_LIST_BTN_TXT,
    EDIT_BTN_TXT,
    NO_BTN_TXT,
    REMOVE_BTN_TXT,
    YES_BTN_TXT,
)

from .states import (
    CreateMedicamentSG,
    GetOwnMedicamentSG,
    GetOwnMedicamentsSG,
    start_update_medicament,
    start_view_medicament,
)

# Common getters and handlers


@inject
async def get_medicaments(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs):
    medicaments: list[OwnMedicamentDTO] = await sender.send_query(GetOwnMedicamentsDTO(pagination=Pagination()))
    return {"medicaments": medicaments}


@inject
async def get_current_medicament(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs):
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    medicament_id: UUID = dialog_manager.start_data["medicament_id"]
    medicament = await sender.send_query(GetOwnMedicamentDTO(id=medicament_id))
    return {"medicament": medicament}


""" List Medicaments Dialog """


async def on_medicament_selected(_: CallbackQuery, __: Any, dialog_manager: DialogManager, medicament_id: str):
    await start_view_medicament(dialog_manager, UUID(medicament_id))


list_medicaments_dialog = Dialog(
    Window(
        Const("💊 Ваши медикаменты:"),
        ScrollingGroup(
            Select(
                Format("{item.name} | {item.dosage}"),
                id="s_medicaments",
                item_id_getter=lambda x: str(x.id),
                items="medicaments",
                on_click=on_medicament_selected,
            ),
            id="scroll_meds",
            width=1,
            height=PAGE_SIZE,
            hide_on_single_page=True,
        ),
        Start(Const(ADD_BTN_TXT), id="btn_add_med", state=CreateMedicamentSG.name),
        Cancel(Const(BACK_BTN_TXT)),
        state=GetOwnMedicamentsSG.view,
        getter=get_medicaments,
    )
)


"""View Medicament Dialog"""


async def on_update_clicked(_: CallbackQuery, __: Button, dialog_manager: DialogManager):
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    medicament_id: UUID = dialog_manager.start_data["medicament_id"]
    await start_update_medicament(dialog_manager, medicament_id)


async def on_delete_clicked(_: CallbackQuery, __: Button, manager: DialogManager):
    await manager.switch_to(GetOwnMedicamentSG.confirm_delete)


@inject
async def on_delete_confirmed(callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]):
    if not isinstance(manager.start_data, dict):
        raise AppError
    medicament_id: UUID = manager.start_data["medicament_id"]
    await sender.send_command(DeleteMedicamentCommand(medicament_id))
    await callback.answer("Медикамент удален")
    await manager.done()


view_medicament_dialog = Dialog(
    Window(
        Jinja(
            """
<b>💊 Медикамент:</b>
<b>Название:</b> {{ medicament.name }}
<b>Дозировка:</b> {{ medicament.dosage }}
"""
        ),
        Row(
            Button(Const(REMOVE_BTN_TXT), id="btn_delete", on_click=on_delete_clicked),
            Button(Const(EDIT_BTN_TXT), id="btn_edit", on_click=on_update_clicked),
        ),
        Cancel(Const(BACK_TO_LIST_BTN_TXT)),
        state=GetOwnMedicamentSG.view,
        getter=get_current_medicament,
        parse_mode="HTML",
    ),
    Window(
        Const("Вы уверены, что хотите удалить этот медикамент?"),
        Row(
            Button(Const(YES_BTN_TXT), id="btn_confirm_delete", on_click=on_delete_confirmed),
            Back(Const(NO_BTN_TXT)),
        ),
        state=GetOwnMedicamentSG.confirm_delete,
    ),
)
