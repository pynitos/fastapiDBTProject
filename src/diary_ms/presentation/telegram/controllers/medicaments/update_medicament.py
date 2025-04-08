from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.medicament.dto.commands.update_medicament import UpdateMedicamentCommand
from src.diary_ms.presentation.telegram.common.constants import (
    CANCEL_BTN_TXT,
    CONFIRM_BTN_TXT,
    EDIT_BTN_TXT,
)

from .states import UpdateMedicamentSG


async def on_edit_name_entered(_: Message, __: ManagedTextInput, manager: DialogManager, name: str):
    manager.dialog_data["name"] = name
    await manager.next()


async def on_edit_dosage_entered(_: Message, __: ManagedTextInput, manager: DialogManager, dosage: str):
    manager.dialog_data["dosage"] = dosage
    await manager.next()


@inject
async def on_edit_confirmed(callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]):
    await sender.send_command(
        UpdateMedicamentCommand(
            id=manager.dialog_data["medicament_id"],
            name=manager.dialog_data["name"],
            dosage=manager.dialog_data["dosage"],
        )
    )
    await callback.answer("Медикамент обновлен")
    await manager.done()


update_medicament_dialog = Dialog(
    Window(
        Const("Введите новое название:"),
        TextInput(id="input_name", on_success=on_edit_name_entered),
        Cancel(Const("❌ Отмена")),
        state=UpdateMedicamentSG.name,
    ),
    Window(
        Const("Введите новую дозировку:"),
        TextInput(id="input_dosage", on_success=on_edit_dosage_entered),
        Back(Const("◀️ Назад")),
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
            Button(Const(CONFIRM_BTN_TXT), id="btn_confirm", on_click=on_edit_confirmed),
            Cancel(Const(CANCEL_BTN_TXT)),
        ),
        state=UpdateMedicamentSG.preview,
        parse_mode="HTML",
    ),
)
