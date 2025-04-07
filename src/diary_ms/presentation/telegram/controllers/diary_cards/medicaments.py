from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.medicament.dto.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.application.medicament.dto.commands.delete_medicament import DeleteMedicamentCommand
from src.diary_ms.application.medicament.dto.commands.update_medicament import UpdateMedicamentCommand
from src.diary_ms.application.medicament.dto.medicament import GetOwnMedicamentDTO, GetOwnMedicamentsDTO
from src.diary_ms.presentation.telegram.common.constants import CANCEL_BTN_TXT

from .states import MedicamentSG


async def on_medicament_selected(_: CallbackQuery, __: Any, manager: DialogManager, medicament_id: str):
    manager.dialog_data["medicament_id"] = medicament_id
    await manager.switch_to(MedicamentSG.view_medicament)


async def on_delete_clicked(callback: CallbackQuery, _: Button, manager: DialogManager):
    await manager.switch_to(MedicamentSG.confirm_delete)


@inject
async def on_delete_confirmed(callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]):
    medicament_id = manager.dialog_data["medicament_id"]
    await sender.send_command(DeleteMedicamentCommand(medicament_id))
    await callback.answer("Медикамент удален")
    await manager.done()


async def on_add_name_entered(_: Message, __: ManagedTextInput, 
                            manager: DialogManager, name: str):
    manager.dialog_data["add_name"] = name
    await manager.next()

async def on_add_dosage_entered(_: Message, __: ManagedTextInput, 
                              manager: DialogManager, dosage: str):
    manager.dialog_data["add_dosage"] = dosage
    await manager.next()


async def on_edit_name_entered(_: Message, __: ManagedTextInput, 
                               manager: DialogManager, dosage: str):
    manager.dialog_data["edit_name"] = dosage
    await manager.next()


async def on_edit_dosage_entered(_: Message, __: ManagedTextInput, 
                               manager: DialogManager, dosage: str):
    manager.dialog_data["edit_dosage"] = dosage
    await manager.next()

@inject
async def on_add_confirmed(callback: CallbackQuery, button: Button, 
                         manager: DialogManager, sender: FromDishka[Sender]):
    # Вызов use case для добавления
    await sender.send_command(
        CreateMedicamentCommand(
            name=manager.dialog_data["add_name"],
            dosage=manager.dialog_data["add_dosage"]
        )
    )
    await callback.answer("Медикамент добавлен")
    await manager.done()


@inject
async def on_edit_confirmed(callback: CallbackQuery, button: Button, 
                          manager: DialogManager, sender: FromDishka[Sender]):
    await sender.send_command(
        UpdateMedicamentCommand(
            id=manager.dialog_data["medicament_id"],
            name=manager.dialog_data["name"],
            dosage=manager.dialog_data["dosage"]
        )
    )
    await callback.answer("Медикамент обновлен")
    await manager.done()


@inject
async def get_medicaments(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs):
    medicaments = await sender.send_query(GetOwnMedicamentsDTO(pagination=Pagination()))
    return {"medicaments": medicaments}


@inject
async def get_current_medicament(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs):
    medicament_id = dialog_manager.dialog_data["medicament_id"]
    # Здесь получаем детали медикамента из use case
    medicament = await sender.send_query(GetOwnMedicamentDTO(id=medicament_id))
    return {"medicament": {"name": medicament.name, "dosage": medicament.dosage}}


# Windows
list_window = Window(
    Const("💊 Ваши медикаменты:"),
    ScrollingGroup(
        Select(
            Format("{item.name} ({item.dosage})"),
            id="s_medicaments",
            item_id_getter=lambda x: str(x.id),
            items="medicaments",
            on_click=on_medicament_selected,
        ),
        id="scroll_meds",
        width=1,
        height=5,
        hide_on_single_page=True,
    ),
    SwitchTo(Const("➕ Добавить"), id="btn_add", state=MedicamentSG.add_name),
    Cancel(Const("◀️ Назад")),
    state=MedicamentSG.list_medicaments,
    getter=get_medicaments,
)

view_window = Window(
    Jinja(
        """
<b>💊 Медикамент:</b>
<b>Название:</b> {{ medicament.name }}
<b>Дозировка:</b> {{ medicament.dosage }}
"""
    ),
    Row(
        SwitchTo(Const("✏️ Редактировать"), id="btn_edit", state=MedicamentSG.edit_name),
        Button(Const("🗑 Удалить"), id="btn_delete", on_click=on_delete_clicked),
    ),
    Back(Const("◀️ К списку")),
    state=MedicamentSG.view_medicament,
    getter=get_current_medicament,
    parse_mode="HTML",
)

add_windows = (
    Window(
    Const("Введите название медикамента:"),
    TextInput(id="add_name", on_success=on_add_name_entered),
    Cancel(Const(CANCEL_BTN_TXT)),
    state=MedicamentSG.add_name,
    ),
    Window(
    Const("Введите дозировку и способ применения медикамента:"),
    TextInput(id="add_dosage", on_success=on_add_dosage_entered),
    Cancel(Const("◀️ Отмена")),
    state=MedicamentSG.add_dosage,
    ),
    Window(
    Jinja(
        """
<b>Подтвердите добавление медикамента:</b>
💊 <b>Название:</b> {{ dialog_data["add_name"] }}
📊 <b>Дозировка:</b> {{ dialog_data["add_dosage"] }}
"""
    ),
    Row(
        Button(Const("✅ Подтвердить"), id="btn_confirm_add", on_click=on_add_confirmed),
        Button(Const("✏️ Изменить"), id="btn_edit_add", on_click=lambda c, b, m: m.switch_to(MedicamentSG.add_medicament_name)),
    ),
    state=MedicamentSG.confirm_add,
    parse_mode="HTML"
)
    )
edit_window = Window(
    Const("Введите новую дозировку:"),
    TextInput(id="edit_dosage", on_success=on_edit_dosage_entered),
    Cancel(Const(CANCEL_BTN_TXT)),
    state=MedicamentSG.edit_dosage,
)

confirm_delete_window = Window(
    Const("Вы уверены, что хотите удалить этот медикамент?"),
    Row(
        Button(Const("✅ Да"), id="btn_confirm_delete", on_click=on_delete_confirmed),
        Back(Const("❌ Нет")),
    ),
    state=MedicamentSG.confirm_delete,
)

# Dialog setup
medicament_dialog = Dialog(list_window, view_window, *add_windows, edit_window, confirm_delete_window)
