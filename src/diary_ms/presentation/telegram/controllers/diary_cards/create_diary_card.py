import operator
from dataclasses import asdict
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Select
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery

from . import states


async def get_mood_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    # Предоставляем пользователю выбор из пяти вариантов настроения
    moods = [
        ("1 — Очень плохое", 1),
        ("2 — Плохое", 2),
        ("3 — Нейтральное", 3),
        ("4 — Хорошее", 4),
        ("5 — Отличное", 5),
    ]
    return {"moods": moods}


async def on_mood_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: int):
    # Сохраняем выбранное настроение как число
    manager.dialog_data["mood"] = selected
    await manager.next()


async def get_description_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    # Логика для получения данных о описании
    return {}


async def on_description_entered(call: CallbackQuery, widget: Button, manager: DialogManager):
    # Логика обработки введенного описания
    await manager.next()


async def get_data(sender: FromDishka[Sender], **kwargs) -> dict[str, Any]:
    d: DataForDiaryCardDTO = await sender.send_query(GetDataForDiaryCardQuery())
    emotions: list[dict[str, Any]] = [asdict(x) for x in d.emotions]
    skills: list[dict[str, Any]] = [asdict(x) for x in d.skills]
    targets: list[dict[str, Any]] = [asdict(x) for x in d.targets]
    medicaments: list[dict[str, Any]] = [asdict(x) for x in d.medicaments]
    return {
        "emotions": emotions,
        "skills": skills,
        "targets": targets,
        "medicaments": medicaments,
    }


async def on_targets_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("targets", []).append(selected)
    await manager.next()


async def on_emotions_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("emotions", []).append(selected)
    await manager.next()


async def on_medicaments_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("medicaments", []).append(selected)
    await manager.next()


async def on_skills_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("skills", []).append(selected)
    await manager.next()


async def get_confirmation_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    # Преобразуем число в текстовое описание для отображения
    mood_mapping = {
        1: "1 — Очень плохое",
        2: "2 — Плохое",
        3: "3 — Нейтральное",
        4: "4 — Хорошее",
        5: "5 — Отличное",
    }
    mood = dialog_manager.dialog_data.get("mood", "Не указано")
    mood_text = mood_mapping.get(mood, "Не указано")

    return {
        "mood": mood_text,  # Отображаем текстовое описание
        "description": dialog_manager.dialog_data.get("description", "Не указано"),
        "targets": dialog_manager.dialog_data.get("targets", []),
        "emotions": dialog_manager.dialog_data.get("emotions", []),
        "medicaments": dialog_manager.dialog_data.get("medicaments", []),
        "skills": dialog_manager.dialog_data.get("skills", []),
    }


@inject
async def on_confirmation(
    call: CallbackQuery, widget: Button, manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    # Логика подтверждения и сохранения данных
    await sender.send_command(
        CreateDiaryCardCommand(
            mood=manager.dialog_data["mood"],
            description=manager.dialog_data["description"],
            targets=manager.dialog_data["targets"],
            emotions=manager.dialog_data["emotions"],
            medicaments=manager.dialog_data["medicaments"],
            skills=manager.dialog_data["skills"],
        )
    )
    await manager.done()


diary_card_dialog = Dialog(
    Window(
        Const("Выберите ваше настроение:"),
        Select(
            id="select_mood",
            text=Format("{item[0]}"),  # Отображаем текстовое описание настроения
            items="moods",
            item_id_getter=operator.itemgetter(1),  # Используем число как идентификатор
            on_click=on_mood_selected,
            type_factory=int,
        ),
        Cancel(Const("Отмена")),
        getter=get_mood_data,
        state=states.CreateDiaryCardSG.mood,
    ),
    Window(
        Const("Опишите ваше состояние:"),
        Button(Const("Далее"), on_click=on_description_entered, id="next_description"),
        Back(Const("Назад")),
        getter=get_description_data,
        state=states.CreateDiaryCardSG.description,
    ),
    Window(
        Const("Выберите ваши цели:"),
        Select(
            id="select_targets",
            text=Format("{item}"),
            items="targets",
            item_id_getter=lambda x: x,
            on_click=on_targets_selected,
        ),
        Back(Const("Назад")),
        getter=get_data,
        state=states.CreateDiaryCardSG.targets,
    ),
    Window(
        Const("Выберите ваши медикаменты:"),
        Select(
            id="select_medicaments",
            text=Format("{item}"),
            items="medicaments",
            item_id_getter=lambda x: x,
            on_click=on_medicaments_selected,
        ),
        Back(Const("Назад")),
        getter=get_data,
        state=states.CreateDiaryCardSG.medicaments,
    ),
    Window(
        Const("Выберите ваши навыки:"),
        Select(
            id="select_skills",
            text=Format("{item}"),
            items="skills",
            item_id_getter=lambda x: x,
            on_click=on_skills_selected,
        ),
        Back(Const("Назад")),
        getter=get_data,
        state=states.CreateDiaryCardSG.skills,
    ),
    Window(
        Const("Проверьте введенные данные:"),
        Format("Настроение: {mood}"),
        Format("Описание: {description}"),
        Format("Цели: {targets}"),
        Format("Эмоции: {emotions}"),
        Format("Медикаменты: {medicaments}"),
        Format("Навыки: {skills}"),
        Button(Const("Подтвердить"), on_click=on_confirmation, id="confirm"),
        Back(Const("Назад")),
        getter=get_confirmation_data,
        state=states.CreateDiaryCardSG.CONFIRMATION,
    ),
)
