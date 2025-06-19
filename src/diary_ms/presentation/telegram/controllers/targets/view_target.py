from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.target_behavior.dto.target_behavior import GetOwnTargetQuery
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.presentation.telegram.common.constants import BACK_TO_LIST_BTN_TXT, EDIT_BTN_TXT, REMOVE_BTN_TXT
from src.diary_ms.presentation.telegram.common.constants.targets import TARGET_HEADER

from .delete_target import delete_target_window
from .states import ViewTargetSG, start_update_target


@inject
async def get_target_data(
    dialog_manager: DialogManager,
    sender: FromDishka[Sender],
    **kwargs: Any,  # noqa: ARG001
) -> dict[str, Any]:
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    target = await sender.send_query(GetOwnTargetQuery(id=UUID(dialog_manager.start_data["target_id"])))
    return {
        "target": {
            "urge": target.urge,
            "action": target.action or "не указано",
            "header": TARGET_HEADER,
        }
    }


async def on_target_update_clicked(_: CallbackQuery, __: Button, dialog_manager: DialogManager) -> None:
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    t_id: str = dialog_manager.start_data["target_id"]
    await start_update_target(dialog_manager, t_id)


view_target_window = Window(
    Jinja(
        """
<b>{{ target.header }}:</b> {{ target.urge }}

🛡️ <b>Копинг-стратегия:</b> {{ target.action }}
"""
    ),
    Row(
        SwitchTo(Const(REMOVE_BTN_TXT), id="btn_delete", state=ViewTargetSG.confirm_delete),
        Button(Const(EDIT_BTN_TXT), id="btn_edit", on_click=on_target_update_clicked),
    ),
    Cancel(Const(BACK_TO_LIST_BTN_TXT)),
    state=ViewTargetSG.view,
    getter=get_target_data,
    parse_mode="HTML",
)

get_target_dialog = Dialog(view_target_window, delete_target_window)
