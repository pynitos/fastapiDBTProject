import operator
import logging
from dataclasses import asdict
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Column, Multiselect, Next, Row, Select
from aiogram_dialog.widgets.kbd.select import ManagedMultiselect
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery
from src.diary_ms.presentation.telegram.common.constants import BACK_BTN_TXT, CANCEL_BTN_TXT, NEXT_BTN_TXT

from . import states

logger = logging.getLogger(__name__)


async def get_mood_data(**kwargs) -> dict[str, Any]:
    # Предоставляем пользователю выбор из пяти вариантов настроения
    moods = [
        ("Отличное", 5),
        ("Хорошее", 4),
        ("Нейтральное", 3),
        ("Плохое", 2),
        ("Очень плохое", 1),
    ]
    return {"moods": moods}


async def on_mood_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: int):
    # Сохраняем выбранное настроение как число
    manager.dialog_data["mood"] = selected
    await manager.next()


async def on_description_entered(
    message: Message,  # noqa: ARG001
    widget: ManagedTextInput[str],  # noqa: ARG001
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data["description"] = data
    await dialog_manager.next()


@inject
async def get_data(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs) -> dict[str, Any]:
    d: DataForDiaryCardDTO = await sender.send_query(GetDataForDiaryCardQuery())
    emotions: list[dict[str, Any]] = [asdict(x) for x in d.emotions]
    skills: list[dict[str, Any]] = [asdict(x) for x in d.skills]
    targets: list[dict[str, Any]] = [asdict(x) for x in d.targets]
    medicaments: list[dict[str, Any]] = [asdict(x) for x in d.medicaments]

    dialog_manager.dialog_data["emotions"] = emotions

    return {
        "emotions": emotions,
        "skills": skills,
        "targets": targets,
        "medicaments": medicaments,
    }


async def on_target_selected(callback: CallbackQuery, widget: Select, manager: DialogManager, selected_id: str):
    targets = manager.dialog_data["targets"]
    selected_target = next(t for t in targets if str(t["id"]) == selected_id)
    manager.dialog_data["selected_target"] = selected_target
    await manager.next()


async def on_emotion_selected(
    _: CallbackQuery,
    __: ManagedMultiselect[str],
    dialog_manager: DialogManager,
    data: list[str],
) -> None:
    logger.info(data)
    dialog_manager.dialog_data.setdefault("selected_emotions", []).extend([
        e for e in dialog_manager.dialog_data["emotions"] if str(e["id"]) in data
    ])


async def on_medicaments_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("medicaments", []).append(selected)
    await manager.next()


async def on_skills_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("skills", []).append(selected)
    await manager.next()


async def get_confirmation_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    # Преобразуем число в текстовое описание для отображения
    mood_mapping = {
        1: "Очень плохое",
        2: "Плохое",
        3: "Нейтральное",
        4: "Хорошее",
        5: "Отличное",
    }
    mood = dialog_manager.dialog_data.get("mood", "Не указано")
    mood_text = mood_mapping.get(mood, "Не указано")
    emotions = dialog_manager.dialog_data.get("selected_emotions", [])

    selected_emotions = [e.get('name') for e in emotions]

    return {
        "mood": mood_text,  # Отображаем текстовое описание
        "description": dialog_manager.dialog_data.get("description", "Не указано"),
        "targets": dialog_manager.dialog_data.get("targets", []),
        "selected_emotions": selected_emotions,
        "medicaments": dialog_manager.dialog_data.get("medicaments", []),
        "skills": dialog_manager.dialog_data.get("skills", []),
    }


@inject
async def on_confirmation(
    _: CallbackQuery, __: Button, dialog_manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    emotions = dialog_manager.dialog_data.get("selected_emotions", [])
    emotions_ids = [e.get('id') for e in emotions]
    await sender.send_command(
        CreateDiaryCardCommand(
            mood=dialog_manager.dialog_data["mood"],
            description=dialog_manager.dialog_data.get("description"),
            targets=dialog_manager.dialog_data.get("targets"),
            emotions=emotions_ids,
            medicaments=dialog_manager.dialog_data.get("medicaments"),
            skills=dialog_manager.dialog_data.get("skills"),
        )
    )
    await dialog_manager.next()


DESCRIPTION_INPUT_ID = "description_input_id"
back_next_row = Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT)))

create_diary_card_dialog = Dialog(
    Window(
        Const("Выберите ваше настроение:"),
        Column(
            Select(
                id="select_mood",
                text=Format("{item[0]}"),  # Отображаем текстовое описание настроения
                items="moods",
                item_id_getter=operator.itemgetter(1),  # Используем число как идентификатор
                on_click=on_mood_selected,
                type_factory=int,
            )
        ),
        Cancel(Const(CANCEL_BTN_TXT)),
        getter=get_mood_data,
        state=states.CreateDiaryCardSG.mood,
    ),
    Window(
        Const("Опишите ваше состояние:"),
        back_next_row,
        TextInput[str](id=DESCRIPTION_INPUT_ID, on_success=on_description_entered),
        state=states.CreateDiaryCardSG.description,
    ),
    Window(
        Const("Выберите  ключевые эмоции за день:"),
        Column(
            Multiselect(
                Format("✓ {item[name]}"),
                Format("{item[name]}"),
                id="m_emotions",
                item_id_getter=lambda x: str(x["id"]),
                items="emotions",
                on_click=on_emotion_selected, # type: ignore
                )
            ),
        back_next_row,
        state=states.CreateDiaryCardSG.emotions,
    ),
    Window(
        Const("Проверьте введенные данные:"),
        Format("Настроение: {mood}"),
        Format("Описание: {description}"),
        Format("Цели: {targets}"),
        Format("Эмоции: {selected_emotions}"),
        Format("Медикаменты: {medicaments}"),
        Format("Навыки: {skills}"),
        Button(Const("Подтвердить"), on_click=on_confirmation, id="confirm"),
        Back(Const("Назад")),
        getter=get_confirmation_data,
        state=states.CreateDiaryCardSG.CONFIRMATION,
    ),
    Window(
        Const("Дневниковая карточка успешно добавлена!"),
        state=states.CreateDiaryCardSG.DONE,
    ),
    getter=get_data
)
