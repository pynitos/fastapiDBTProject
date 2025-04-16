from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Next, Row
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.target_behavior.dto.commands.update_target import UpdateTargetCommand
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.presentation.telegram.common.constants import (
    CANCEL_BTN_TXT,
    CONFIRM_BTN_TXT,
    NEXT_BTN_TXT,
)

from .states import UpdateTargetSG


async def on_urge_entered(message: Message, _: ManagedTextInput, manager: DialogManager, urge: str):
    manager.dialog_data["urge"] = urge
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


async def on_action_entered(message: Message, _: ManagedTextInput, manager: DialogManager, action: str):
    manager.dialog_data["action"] = action
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


@inject
async def on_update_confirmed(callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]):
    if not isinstance(manager.start_data, dict):
        raise AppError

    await sender.send_command(
        UpdateTargetCommand(
            id=manager.start_data["target_id"],
            urge=manager.dialog_data.get("urge"),
            action=manager.dialog_data.get("action"),
        )
    )
    await callback.answer("Целевое поведение обновлено")
    await manager.done()


update_target_dialog = Dialog(
    Window(
        Const("Опишите проблемное поведение/побуждение:"),
        TextInput(id="upd_urge", on_success=on_urge_entered),
        Row(
            Cancel(Const(CANCEL_BTN_TXT)),
            Next(Const(NEXT_BTN_TXT)),
        ),
        state=UpdateTargetSG.urge,
    ),
    Window(
        Const("Введите альтернативное действие (копинг-стратегию):"),
        TextInput(id="upd_action", on_success=on_action_entered),
        Row(
            Cancel(Const(CANCEL_BTN_TXT)),
            Next(Const(NEXT_BTN_TXT)),
        ),
        state=UpdateTargetSG.action,
    ),
    Window(
        Jinja(
            """
<b>Подтвердите изменения:</b>

🚨 <b>Проблемное поведение:</b> {{ dialog_data["urge"] }}

🛡️ <b>Копинг-стратегия:</b> {{ dialog_data["action"] }}
"""
        ),
        Row(
            Cancel(Const(CANCEL_BTN_TXT)),
            Button(Const(CONFIRM_BTN_TXT), id="btn_confirm", on_click=on_update_confirmed),
        ),
        state=UpdateTargetSG.confirm,
        parse_mode="HTML",
    ),
)
