from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.medicament.dto.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.presentation.telegram.common.constants import (
    BACK_BTN_TXT,
    CANCEL_BTN_TXT,
    CONFIRM_BTN_TXT,
)

from .states import CreateMedicamentSG


async def on_add_name_entered(message: Message, __: ManagedTextInput, manager: DialogManager, name: str):
    manager.dialog_data["name"] = name
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


async def on_add_dosage_entered(message: Message, __: ManagedTextInput, manager: DialogManager, dosage: str):
    manager.dialog_data["dosage"] = dosage
    manager.show_mode = ShowMode.EDIT
    await message.delete()
    await manager.next()


@inject
async def on_add_confirmed(callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]):
    await sender.send_command(
        CreateMedicamentCommand(name=manager.dialog_data["name"], dosage=manager.dialog_data["dosage"])
    )
    await callback.answer("Медикамент добавлен")
    await manager.done()


create_medicament_dialog = Dialog(
    Window(
        Const("Введите название медикамента:"),
        TextInput(id="input_name", on_success=on_add_name_entered),
        Cancel(Const(CANCEL_BTN_TXT)),
        state=CreateMedicamentSG.name,
    ),
    Window(
        Const("Введите дозировку и способ применения:"),
        TextInput(id="input_dosage", on_success=on_add_dosage_entered),
        Back(Const(BACK_BTN_TXT)),
        state=CreateMedicamentSG.dosage,
    ),
    Window(
        Jinja(
            """
<b>Подтвердите добавление медикамента:</b>
💊 <b>Название:</b> {{ dialog_data["name"] }}
📊 <b>Дозировка:</b> {{ dialog_data["dosage"] }}
"""
        ),
        Row(
            Cancel(Const(CANCEL_BTN_TXT)),
            Button(Const(CONFIRM_BTN_TXT), id="btn_confirm", on_click=on_add_confirmed),
        ),
        state=CreateMedicamentSG.preview,
        parse_mode="HTML",
    ),
)
