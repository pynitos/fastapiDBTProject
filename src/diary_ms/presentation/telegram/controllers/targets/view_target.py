from typing import Any

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.target_behavior.dto.target_behavior import GetOwnTargetQuery
from src.diary_ms.presentation.telegram.common.constants import BACK_TO_LIST_BTN_TXT, REMOVE_BTN_TXT
from src.diary_ms.presentation.telegram.common.constants.targets import TARGET_HEADER

from .delete_target import delete_target_window
from .states import ViewTargetSG


@inject
async def get_target_data(
    dialog_manager: DialogManager,
    sender: FromDishka[Sender],
    **kwargs: Any,
) -> dict[str, Any]:
    target = await sender.send_query(GetOwnTargetQuery(id=dialog_manager.start_data["target_id"]))
    return {
        "target": {
            "urge": target.urge,
            "action": target.action or "не указано",
            "header": TARGET_HEADER,
        }
    }


view_target_window = Window(
    Jinja(
        """
<b>{{ target.header }}:</b>

<b>Поведение:</b> {{ target.urge }}

<b>Копинг-стратегия:</b> {{ target.action }}
"""
    ),
    SwitchTo(Const(REMOVE_BTN_TXT), id="btn_delete", state=ViewTargetSG.confirm_delete),
    Back(Const(BACK_TO_LIST_BTN_TXT)),
    state=ViewTargetSG.view,
    getter=get_target_data,
    parse_mode="HTML",
)

get_target_dialog = Dialog(view_target_window, delete_target_window)
