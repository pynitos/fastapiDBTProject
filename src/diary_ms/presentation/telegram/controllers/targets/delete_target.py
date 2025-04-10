from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.target_behavior.dto.commands.delete_target import DeleteTargetCommand
from src.diary_ms.presentation.telegram.common.constants import NO_BTN_TXT, YES_BTN_TXT
from src.diary_ms.presentation.telegram.common.constants.targets import TARGET_DELETE_CONFIRM_MSG, TARGET_DELETED_MSG

from .states import TargetViewSG


@inject
async def on_delete_confirmed(
    callback: CallbackQuery,
    _: Button,
    manager: DialogManager,
    sender: FromDishka[Sender],
) -> None:
    await sender.send_command(DeleteTargetCommand(id=manager.dialog_data["target_id"]))
    await callback.answer(TARGET_DELETED_MSG)
    await manager.done()


delete_target_window = Window(
    Const(TARGET_DELETE_CONFIRM_MSG),
    Button(Const(YES_BTN_TXT), id="btn_confirm_delete", on_click=on_delete_confirmed),
    Back(Const(NO_BTN_TXT)),
    state=TargetViewSG.confirm_delete,
)
