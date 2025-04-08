from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Next, Row
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.medicament.dto.commands.update_medicament import UpdateMedicamentCommand
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.presentation.telegram.common.constants import (
    CANCEL_BTN_TXT,
    CONFIRM_BTN_TXT,
    NEXT_BTN_TXT,
)
from src.diary_ms.presentation.telegram.common.widgets.back_next import back_next_row

from .states import UpdateMedicamentSG


async def on_edit_name_entered(message: Message, __: ManagedTextInput, manager: DialogManager, name: str):
    manager.dialog_data["name"] = name
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


async def on_edit_dosage_entered(message: Message, __: ManagedTextInput, manager: DialogManager, dosage: str):
    manager.dialog_data["dosage"] = dosage
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


@inject
async def on_edit_confirmed(
    callback: CallbackQuery, _: Button, dialog_manager: DialogManager, sender: FromDishka[Sender]
):
    print(dialog_manager.start_data)
    if not isinstance(dialog_manager.start_data, dict):
        raise AppError
    await sender.send_command(
        UpdateMedicamentCommand(
            id=dialog_manager.start_data["medicament_id"],
            name=dialog_manager.dialog_data["name"],
            dosage=dialog_manager.dialog_data["dosage"],
        )
    )
    await callback.answer("Медикамент обновлен")
    await dialog_manager.done()


update_medicament_dialog = Dialog(
    Window(
        Const("Введите новое название:"),
        TextInput(id="input_name", on_success=on_edit_name_entered),
        Row(Cancel(Const(CANCEL_BTN_TXT)), Next(Const(NEXT_BTN_TXT))),
        state=UpdateMedicamentSG.name,
    ),
    Window(
        Const("Введите новую дозировку:"),
        TextInput(id="input_dosage", on_success=on_edit_dosage_entered),
        back_next_row(),
        state=UpdateMedicamentSG.dosage,
    ),
    Window(
        Jinja(
            """
<b>Подтвердите изменения:</b>
💊 <b>Название:</b> {{ dialog_data["name"] }}
📊 <b>Дозировка:</b> {{ dialog_data["dosage"] }}
"""
        ),
        Row(
            Cancel(Const(CANCEL_BTN_TXT)),
            Button(Const(CONFIRM_BTN_TXT), id="btn_confirm", on_click=on_edit_confirmed),
        ),
        state=UpdateMedicamentSG.preview,
        parse_mode="HTML",
    ),
)
