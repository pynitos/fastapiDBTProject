from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from diary_ms.application.common.interfaces.dispatcher.base import Sender
from diary_ms.application.target_behavior.dto.commands.delete_target import DeleteTargetCommand
from diary_ms.presentation.telegram.common.constants import NO_BTN_TXT, YES_BTN_TXT
from diary_ms.presentation.telegram.common.constants.targets import TARGET_DELETE_CONFIRM_MSG, TARGET_DELETED_MSG

from .states import ViewTargetSG


@inject
async def on_delete_confirmed(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    sender: FromDishka[Sender],
) -> None:
    if not isinstance(dialog_manager.start_data, dict):
        await callback.answer("ERROR!")
        await dialog_manager.done()
        return
    await sender.send_command(DeleteTargetCommand(id=dialog_manager.start_data["target_id"]))
    await callback.answer(TARGET_DELETED_MSG)
    await dialog_manager.done()


delete_target_window = Window(
    Const(TARGET_DELETE_CONFIRM_MSG),
    Button(Const(YES_BTN_TXT), id="btn_confirm_delete", on_click=on_delete_confirmed),
    Back(Const(NO_BTN_TXT)),
    state=ViewTargetSG.confirm_delete,
)
