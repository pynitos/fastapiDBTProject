from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.target_behavior.dto.commands.create_target import CreateTargetCommand
from src.diary_ms.presentation.telegram.common.constants import CANCEL_BTN_TXT, CONFIRM_BTN_TXT
from src.diary_ms.presentation.telegram.common.constants.targets import (
    TARGET_COPING_STRATEGY_PROMPT,
    TARGET_URGE_PROMPT,
)
from src.diary_ms.presentation.telegram.common.widgets.back_next import back_next_row

from .states import CreateTargetSG


@inject
async def on_urge_entered(
    message: Message,
    _: Any,
    manager: DialogManager,
    urge: str,
) -> None:
    manager.dialog_data["urge"] = urge
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


@inject
async def on_action_entered(
    message: Message,
    _: Any,
    manager: DialogManager,
    action: str,
) -> None:
    manager.dialog_data["action"] = action
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


create_urge_window = Window(
    Const(TARGET_URGE_PROMPT),
    TextInput(id="input_urge", on_success=on_urge_entered),
    Cancel(Const(CANCEL_BTN_TXT)),
    state=CreateTargetSG.urge,
)

create_action_window = Window(
    Const(TARGET_COPING_STRATEGY_PROMPT),
    TextInput(id="input_action", on_success=on_action_entered),
    back_next_row(),
    state=CreateTargetSG.action,
)


@inject
async def on_create_confirmed(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    sender: FromDishka[Sender],
) -> None:
    await sender.send_command(
        CreateTargetCommand(
            urge=dialog_manager.dialog_data["urge"],
            action=dialog_manager.dialog_data.get("action"),
        )
    )
    await callback.answer("Цель создана")
    await dialog_manager.done()


create_confirm_window = Window(
    Jinja(
        """
<b>Подтвердите создание цели:</b>
<b>Поведение:</b> {{ dialog_data["urge"] }}
<b>Действие:</b> {{ dialog_data["action"] }}
"""
    ),
    Button(Const(CONFIRM_BTN_TXT), id="btn_confirm", on_click=on_create_confirmed),
    Cancel(Const(CANCEL_BTN_TXT)),
    state=CreateTargetSG.confirm,
    parse_mode="HTML",
)

create_target_dialog = Dialog(create_urge_window, create_action_window, create_confirm_window)
