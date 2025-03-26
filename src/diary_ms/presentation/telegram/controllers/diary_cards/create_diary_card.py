import operator
import logging
from dataclasses import asdict
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Column, Multiselect, Next, Row, Select
from aiogram_dialog.widgets.kbd.select import ManagedMultiselect
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery
from src.diary_ms.presentation.telegram.common.constants import BACK_BTN_TXT, CANCEL_BTN_TXT, NEXT_BTN_TXT, CONFIRM_BTN_TXT

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
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data["description"] = data
    dialog_manager.show_mode=ShowMode.EDIT
    await message.delete()
    await dialog_manager.next()


@inject
async def get_data(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs) -> dict[str, Any]:
    d: DataForDiaryCardDTO = await sender.send_query(GetDataForDiaryCardQuery())
    emotions: list[dict[str, Any]] = [asdict(x) for x in d.emotions]
    skills: list[dict[str, Any]] = [asdict(x) for x in d.skills]
    targets: list[dict[str, Any]] = [asdict(x) for x in d.targets]
    medicaments: list[dict[str, Any]] = [asdict(x) for x in d.medicaments]

    dialog_manager.dialog_data["emotions"] = emotions
    dialog_manager.dialog_data["skills"] = skills

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
    dialog_manager.dialog_data.setdefault("selected_emotions", []).extend([
        e for e in dialog_manager.dialog_data["emotions"] if str(e["id"]) in data
    ])


async def on_medicaments_selected(call: CallbackQuery, widget: Select, manager: DialogManager, selected: str):
    manager.dialog_data.setdefault("medicaments", []).append(selected)
    await manager.next()


async def on_skill_selected(
    _: CallbackQuery,
    __: ManagedMultiselect[str],
    dialog_manager: DialogManager,
    data: list[str],
) -> None:
    dialog_manager.dialog_data.setdefault("selected_skills", []).extend([
        s for s in dialog_manager.dialog_data["skills"] if str(s["id"]) in data
    ])


async def on_skills_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    if 'selected_skills' not in dialog_manager.dialog_data:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.skill_description)


async def skill_name_getter(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    selected_skills = dialog_manager.dialog_data["selected_skills"]
    skill_name = selected_skills[0]['name']
    return {"skill_name": skill_name}

async def on_skill_description_entered(
    message: Message,
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    selected_skills: list[dict[str, Any]] = dialog_manager.dialog_data["selected_skills"]
    skill = selected_skills.pop(0)
    skill['description'] = data
    dialog_manager.dialog_data.setdefault("skills_for_confirm", []).append(skill)
    await message.delete()
    dialog_manager.show_mode=ShowMode.EDIT
    if len(selected_skills) > 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.skill_description)
    else:
        await dialog_manager.next()


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
    skills = dialog_manager.dialog_data.get("skills_for_confirm", [])
    return {
        "mood": mood_text,  # Отображаем текстовое описание
        "description": dialog_manager.dialog_data.get("description", "Не указано"),
        "targets": dialog_manager.dialog_data.get("targets", []),
        "emotions": emotions,
        "medicaments": dialog_manager.dialog_data.get("medicaments", []),
        "skills": skills
    }


@inject
async def on_confirmation(
    _: CallbackQuery, __: Button, dialog_manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    emotions = dialog_manager.dialog_data.get("selected_emotions", [])
    emotions_ids = [e.get('id') for e in emotions]
    skills = dialog_manager.dialog_data.get("skills_for_confirm", [])
    skills_for_create = [
        CreateDiaryCardCommand.Skill(
            id=s['id'], situation=s.get("descriprtion")
            ) for s in skills
            ]
    await sender.send_command(
        CreateDiaryCardCommand(
            mood=dialog_manager.dialog_data["mood"],
            description=dialog_manager.dialog_data.get("description"),
            targets=dialog_manager.dialog_data.get("targets"),
            emotions=emotions_ids,
            medicaments=dialog_manager.dialog_data.get("medicaments"),
            skills=skills_for_create,
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
        Const("Выберите  применённые навыки:"),
        Column(
            Multiselect(
                Format("✓ {item[name]}"),
                Format("{item[name]}"),
                id="ms_skills",
                item_id_getter=lambda x: str(x["id"]),
                items="skills",
                on_click=on_skill_selected, # type: ignore
                )
            ),
        Row(
            Back(Const(BACK_BTN_TXT)),
            Next(
                Const(NEXT_BTN_TXT),
                on_click=on_skills_next_btn
                )
            ),
        state=states.CreateDiaryCardSG.skills,
    ),
    Window(
        Format("Опишите то, как вы прменили навык: {skill_name}"),
        back_next_row,
        TextInput[str](id='skill_input_id', on_success=on_skill_description_entered),
        state=states.CreateDiaryCardSG.skill_description,
        getter=skill_name_getter
    ),
    Window(
        Jinja(
            """
<b>📋 Проверьте введенные данные:</b>
<b>════════════════════════════</b>
<b>Настроение:</b> {{ mood }}
<b>Описание:</b> {{ description }}
<b>🎯 Цели:</b>
{% if targets %}
{% for target in targets -%}
• {{ target }}
{% endfor %}
{% else %}
- Не указаны
{% endif %}
<b>😊 Эмоции:</b>
{% if emotions %}
{% for emotion in emotions -%}
• {{ emotion.name }}
{% endfor %}
{% else %}
- Не указаны
{% endif %}
<b>💊 Медикаменты:</b>
{% if medicaments %}
{% for med in medicaments -%}
• {{ med }}
{% endfor %}
{% else %}
- Не указаны
{% endif %}
<b>🛠 Навыки:</b>
{% if skills %}
{% for skill in skills -%}
• {{ skill.name }} ✧ {% if skill.description %} {{ skill.description }} {% endif %}
{% endfor %}
{% else %}
- Не указаны
{% endif %}
            """
            ),
        Button(Const(CONFIRM_BTN_TXT), on_click=on_confirmation, id="confirm"),
        Back(Const("Назад")),
        getter=get_confirmation_data,
        state=states.CreateDiaryCardSG.CONFIRMATION,
        parse_mode='HTML',
    ),
    Window(
        Const("Дневниковая карточка успешно добавлена!"),
        state=states.CreateDiaryCardSG.DONE,
    ),
    getter=get_data
)
