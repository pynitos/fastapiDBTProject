from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Data, Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Next, Row, Start
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand

from . import states

MOOD_INPUT_ID = "mood"


async def preview_getter(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, Any]:
    mood: ManagedTextInput = dialog_manager.find(MOOD_INPUT_ID)
    return {
        "mood": mood.get_value(),
    }


@inject
async def on_done(
    event: CallbackQuery, button: Button, dialog_manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    mood: ManagedTextInput = dialog_manager.find(MOOD_INPUT_ID)
    await sender.send_command(CreateDiaryCardCommand(mood=int(mood.get_value())))


async def on_view_closed(
    start_data: Data,
    result: Any,
    dialog_manager: DialogManager,
):
    await dialog_manager.done()


create_diary_card_dialog = Dialog(
    Window(
        Format("You are going to create a new diary card.\n\n" "Please, provide mood:"),
        Cancel(),
        TextInput(id=MOOD_INPUT_ID, on_success=Next()),
        preview_add_transitions=[
            Next(),
        ],
        state=states.CreateDiaryCardState.mood,
    ),
    Window(
        Format("You are going to create a new card with mood: " "{mood}\n\n" "Please, confirm or provide new mood."),
        Row(Button(text=Const("Ok"), id="ok", on_click=on_done), Cancel()),
        TextInput(id=MOOD_INPUT_ID),
        preview_add_transitions=[
            Start(Const("0"), state=states.GetOwnDiaryCardsState.view, id="0"),
        ],
        getter=[preview_getter],
        state=states.CreateDiaryCardState.preview,
    ),
    on_process_result=on_view_closed,
)
