from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.dto.pagination import PAGE_SIZE, Pagination
from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnTargetsQuery,
    OwnTargetDTO,
)
from src.diary_ms.presentation.telegram.common.constants import ADD_BTN_TXT, BACK_BTN_TXT
from src.diary_ms.presentation.telegram.common.constants.targets import TARGET_LIST_HEADER
from src.diary_ms.presentation.telegram.controllers.targets.states import (
    CreateTargetSG,
    GetTargetsSG,
    start_view_target,
)


@inject
async def get_targets_data(
    sender: FromDishka[Sender],
    **kwargs: Any,  # noqa: ARG001
) -> dict[str, Any]:
    targets: list[OwnTargetDTO] = await sender.send_query(GetOwnTargetsQuery(pagination=Pagination()))
    return {"targets": targets}


async def on_target_selected(
    _: CallbackQuery,
    __: Any,
    dialog_manager: DialogManager,
    target_id: str,
) -> None:
    await start_view_target(dialog_manager, UUID(target_id))


list_window = Window(
    Const(TARGET_LIST_HEADER),
    ScrollingGroup(
        Select(
            Format("{item.urge}"),
            id="s_targets",
            item_id_getter=lambda item: str(item.id),
            items="targets",
            on_click=on_target_selected,
        ),
        id="targets_sg",
        width=1,
        height=PAGE_SIZE,
        hide_on_single_page=True,
    ),
    Start(Const(ADD_BTN_TXT), id="add_target_btn", state=CreateTargetSG.urge),
    Cancel(Const(BACK_BTN_TXT)),
    state=GetTargetsSG.view,
    getter=get_targets_data,
)

get_targets_dialog = Dialog(list_window)
