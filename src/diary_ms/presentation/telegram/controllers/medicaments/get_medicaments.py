from typing import Any
from uuid import UUID

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Group,
    NumberedPager,
    Row,
    Select,
    Start,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from diary_ms.application.common.dto.pagination import PAGE_SIZE, Pagination
from diary_ms.application.common.interfaces.dispatcher.base import Sender
from diary_ms.application.medicament.dto.commands.delete_medicament import DeleteMedicamentCommand
from diary_ms.application.medicament.dto.medicament import (
    GetOwnMedicamentDTO,
    GetOwnMedicamentsDTO,
    OwnMedicamentDTO,
    OwnMedicamentsDTO,
)
from diary_ms.domain.common.exceptions.base import AppError
from diary_ms.presentation.telegram.common.constants import (
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

MEDICAMENTS_SCROLL_ID = "meds_scroll_id"


@inject
async def get_medicaments(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
    scroll: ManagedScroll | None = dialog_manager.find(MEDICAMENTS_SCROLL_ID)
    page: int = await scroll.get_page() if scroll else 1
    offset: int = page * PAGE_SIZE
    result: OwnMedicamentsDTO = await sender.send_query(GetOwnMedicamentsDTO(pagination=Pagination(offset=offset)))
    return {
        "medicaments": result.medicaments,
        "total": result.total,
        "pages": result.total // PAGE_SIZE + bool(result.total % PAGE_SIZE),
    }


@inject
async def get_current_medicament(
    dialog_manager: DialogManager,
    sender: FromDishka[Sender],
    **kwargs: Any,  # noqa: ARG001
) -> dict[str, Any]:
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    medicament_id: str = dialog_manager.start_data["medicament_id"]
    medicament: OwnMedicamentDTO = await sender.send_query(GetOwnMedicamentDTO(id=UUID(medicament_id)))
    return {"name": medicament.name, "dosage": medicament.dosage}


""" List Medicaments Dialog """


async def on_medicament_selected(_: CallbackQuery, __: Any, dialog_manager: DialogManager, medicament_id: str) -> None:
    await start_view_medicament(dialog_manager, medicament_id)


list_medicaments_dialog = Dialog(
    Window(
        Const("💊 Ваши медикаменты:", when=F["total"]),
        Const("💊 У вас ещё нет медикаментов.", when=~F["total"]),
        StubScroll(id=MEDICAMENTS_SCROLL_ID, pages=F["pages"]),
        Column(
            Select(
                Format("{item.name} | {item.dosage}"),
                id="s_medicaments",
                item_id_getter=lambda x: str(x.id),
                items="medicaments",
                on_click=on_medicament_selected,
            ),
        ),
        Group(
            NumberedPager(id="pager_targets", scroll=MEDICAMENTS_SCROLL_ID),
            width=8,
        ),
        Start(Const(ADD_BTN_TXT), id="btn_add_med", state=CreateMedicamentSG.name),
        Cancel(Const(BACK_BTN_TXT)),
        state=GetOwnMedicamentsSG.view,
        getter=get_medicaments,
    )
)


"""View Medicament Dialog"""


async def on_update_clicked(_: CallbackQuery, __: Button, dialog_manager: DialogManager) -> None:
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    medicament_id: UUID = dialog_manager.start_data["medicament_id"]
    await start_update_medicament(dialog_manager, medicament_id)


@inject
async def on_delete_confirmed(
    callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]
) -> None:
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
<b>Название:</b> {{ name }}
<b>Дозировка:</b> {{ dosage }}
"""
        ),
        Row(
            SwitchTo(Const(REMOVE_BTN_TXT), id="btn_delete", state=GetOwnMedicamentSG.confirm_delete),
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
