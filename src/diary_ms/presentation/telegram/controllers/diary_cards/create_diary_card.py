import logging
import operator
from dataclasses import asdict
from typing import Any

from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Column, Group, Multiselect, Next, Row, Select
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import (
    CreateCopingStrategyCommand,
    CreateDiaryCardCommand,
    CreateSkillUsageCommand,
)
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery
from src.diary_ms.presentation.telegram.common.constants import (
    BACK_BTN_TXT,
    CANCEL_BTN_TXT,
    CONFIRM_BTN_TXT,
    NEXT_BTN_TXT,
)

from . import states

logger = logging.getLogger(__name__)


async def on_mood_selected(_: CallbackQuery, __: Select, manager: DialogManager, selected: int):
    # Сохраняем выбранное настроение как число
    manager.dialog_data["mood"] = selected
    await manager.next()


async def on_description_entered(
    message: Message,
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data["description"] = data
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()
    await dialog_manager.next()


@inject
async def get_data(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs) -> dict[str, Any]:  # noqa: ARG001
    d: DataForDiaryCardDTO = await sender.send_query(GetDataForDiaryCardQuery())
    emotions: list[dict[str, Any]] = [asdict(x) for x in d.emotions]
    skills: list[dict[str, Any]] = [asdict(x) for x in d.skills]
    targets: list[dict[str, Any]] = [asdict(x) for x in d.targets]
    medicaments: list[dict[str, Any]] = [asdict(x) for x in d.medicaments]
    moods = [
        ("Отличное", 5),
        ("Хорошее", 4),
        ("Нейтральное", 3),
        ("Плохое", 2),
        ("Очень плохое", 1),
    ]

    dialog_manager.dialog_data["emotions"] = emotions
    dialog_manager.dialog_data["skills"] = skills
    dialog_manager.dialog_data["targets"] = targets

    return {
        "moods": moods,
        "emotions": emotions,
        "skills": skills,
        "targets": targets,
        "medicaments": medicaments,
    }


async def on_targets_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
):
    ms_targets = dialog_manager.find("ms_targets")
    selected_ids = ms_targets.get_checked() if ms_targets else []
    if len(selected_ids) == 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.target_effectiveness)
    else:
        targets = [t for t in dialog_manager.dialog_data["targets"] if str(t["id"]) in selected_ids]
        dialog_manager.dialog_data["selected_targets"] = targets


async def target_data_getter(dialog_manager: DialogManager, **kwargs):  # noqa: ARG001
    targets = dialog_manager.dialog_data["selected_targets"]

    current_target = targets[0]
    return {"target_name": current_target["urge"]}


async def on_target_action_entered(
    message: Message,
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    action: str,
):
    targets = dialog_manager.dialog_data["selected_targets"]
    targets[0]["action"] = action  # Сохраняем action для текущей цели
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()
    await dialog_manager.next()


async def on_target_effectiveness_selected(
    _: CallbackQuery,
    __: Select,
    dialog_manager: DialogManager,
    selected: int,  # Выбранное значение (1-10)
):
    targets = dialog_manager.dialog_data["selected_targets"]
    target = targets.pop(0)
    target["effectiveness"] = selected
    dialog_manager.dialog_data.setdefault("targets_for_confirm", []).append(target)
    if targets:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.target_action)
    else:
        await dialog_manager.next()


async def on_target_action_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    targets = dialog_manager.dialog_data["selected_targets"]
    target = targets.pop(0)
    target["action"] = None
    dialog_manager.dialog_data.setdefault("targets_for_confirm", []).append(target)
    if len(targets) > 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.targets)
    else:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.target_effectiveness)


async def on_target_effectiveness_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    targets = dialog_manager.dialog_data["selected_targets"]
    target = targets.pop(0)
    dialog_manager.dialog_data.setdefault("targets_for_confirm", []).append(target)
    if len(targets) > 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.targets)


async def on_skills_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    ms_skill = dialog_manager.find("ms_skills")
    checked_ids = ms_skill.get_checked() if ms_skill else []
    if len(checked_ids) == 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.skill_description)


async def skill_name_getter(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:  # noqa: ARG001
    if "selected_skills" not in dialog_manager.dialog_data:
        ms_skills = dialog_manager.find("ms_skills")
        s_ids = ms_skills.get_checked() if ms_skills else []
        dialog_manager.dialog_data["selected_skills"] = [
            s for s in dialog_manager.dialog_data["skills"] if str(s["id"]) in s_ids
        ]

    selected_skills = dialog_manager.dialog_data["selected_skills"]
    skill_name = selected_skills[0]["name"]
    return {"skill_name": skill_name}


async def on_skill_description_entered(
    message: Message,
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    selected_skills: list[dict[str, Any]] = dialog_manager.dialog_data["selected_skills"]
    skill = selected_skills.pop(0)
    skill["situation"] = data
    dialog_manager.dialog_data.setdefault("skills_for_confirm", []).append(skill)
    await message.delete()
    dialog_manager.show_mode = ShowMode.EDIT
    if len(selected_skills) > 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.skill_description)
    else:
        await dialog_manager.next()


async def on_skill_description_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    selected_skills: list[dict[str, Any]] = dialog_manager.dialog_data["selected_skills"]
    skill = selected_skills.pop(0)
    dialog_manager.dialog_data.setdefault("skills_for_confirm", []).append(skill)
    if len(selected_skills) > 0:
        await dialog_manager.switch_to(states.CreateDiaryCardSG.skills)


async def get_confirmation_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:  # noqa: ARG001
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
    ms_emotions = dialog_manager.find("ms_emotions")
    e_ids = ms_emotions.get_checked() if ms_emotions else []
    emotions = [e for e in dialog_manager.dialog_data["emotions"] if str(e["id"]) in e_ids]
    skills = dialog_manager.dialog_data.get("skills_for_confirm", [])
    targets = dialog_manager.dialog_data.get("targets_for_confirm", [])
    return {
        "mood": mood_text,  # Отображаем текстовое описание
        "description": dialog_manager.dialog_data.get("description", "Не указано"),
        "target_copings": targets,
        "emotions": emotions,
        "medicaments": dialog_manager.dialog_data.get("medicaments", []),
        "skills": skills,
    }


@inject
async def on_confirmation(
    callback: CallbackQuery, __: Button, dialog_manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    emotions = dialog_manager.dialog_data.get("selected_emotions", [])
    emotions_ids = [e.get("id") for e in emotions]
    skills = dialog_manager.dialog_data.get("skills_for_confirm", [])
    skills_for_create = [CreateSkillUsageCommand(id=s["id"], situation=s.get("situation")) for s in skills]
    targets = dialog_manager.dialog_data.get("targets_for_confirm", [])
    targets_for_create = [
        CreateCopingStrategyCommand(
            target_id=t["id"],
            action=t.get("action"),
            effectiveness=t.get("effectiveness"),
        )
        for t in targets
    ]
    await sender.send_command(
        CreateDiaryCardCommand(
            mood=dialog_manager.dialog_data["mood"],
            description=dialog_manager.dialog_data.get("description"),
            targets=targets_for_create,
            emotions=emotions_ids,
            medicaments=dialog_manager.dialog_data.get("medicaments"),
            skills=skills_for_create,
        )
    )

    if not isinstance(callback.message, InaccessibleMessage | None):
        text = str(callback.message.text).replace("Проверьте в", "В") + "\n\n✅ Карточка успешно сохранена!"
        await callback.message.edit_text(text)
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.done()


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
                id="ms_emotions",
                item_id_getter=lambda x: str(x["id"]),
                items="emotions",
            )
        ),
        back_next_row,
        state=states.CreateDiaryCardSG.emotions,
    ),
    Window(
        Const("🎯 Отметьте проблемное поведение:"),
        Column(
            Multiselect(
                Format("✓ {item[urge]}"),
                Format("{item[urge]}"),
                id="ms_targets",
                item_id_getter=lambda x: str(x["id"]),
                items="targets",
            )
        ),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_targets_selected)),
        state=states.CreateDiaryCardSG.targets,
    ),
    Window(
        Format("📌  Поведение: <b>{target_name}.</b>\nОпишите ситуацию и способ совладания с ней:"),
        TextInput(id="target_action_input", on_success=on_target_action_entered),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_target_action_next_btn)),
        state=states.CreateDiaryCardSG.target_action,
        getter=target_data_getter,  # Получаем текущую цель
        parse_mode="HTML",
    ),
    Window(
        Format("📌 Поведение: <b>{target_name}</b>\n\nОцените эффективность:"),
        Group(
            Select(
                Format("{item}"),
                id="select_effectiveness",
                items=list(range(1, 11)),  # Числа от 1 до 10
                item_id_getter=lambda x: x,
                on_click=on_target_effectiveness_selected,
                type_factory=int,
            ),
            width=5,
        ),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_target_effectiveness_next_btn)),
        state=states.CreateDiaryCardSG.target_effectiveness,
        getter=target_data_getter,
        parse_mode="HTML",
    ),
    Window(
        Jinja(
            """
{% if medicaments %}
💊 <b>Выберите принятые медикаменты:</b>
{% else %}
🧪 <b>Медикаменты не указаны.</b>
Вы можете добавить их позже в главном меню.
{% endif %}
            """
        ),
        Column(
            Multiselect(
                Format("✓ {item[name]} | {item[dosage]}"),
                Format("{item[name]} | {item[dosage]}"),
                id="ms_meds",
                item_id_getter=lambda x: str(x["id"]),
                items="medicaments",
            ),
        ),
        back_next_row,
        state=states.CreateDiaryCardSG.medicaments,
        parse_mode="HTML",
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
            )
        ),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_skills_next_btn)),
        state=states.CreateDiaryCardSG.skills,
    ),
    Window(
        Format("Опишите то, как вы прменили навык: {skill_name}"),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_skill_description_next_btn)),
        TextInput[str](id="skill_input_id", on_success=on_skill_description_entered),
        state=states.CreateDiaryCardSG.skill_description,
        getter=skill_name_getter,
    ),
    Window(
        Jinja(
            """
<b>📋 Проверьте введенные данные:</b>
<b>══════════════════════</b>
<b>Настроение:</b> {{ mood }}
<b>Описание:</b> {{ description }}
<b>🎯 Проблемное поведение:</b>
{% if target_copings %}
{% for t in target_copings -%}
• {{ t.urge }} {% if t.action %}
✧ {{ t.action }}{% if t.effectiveness %} | {{ t.effectiveness }}/10{% endif %}
{% endif %}

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

• {{ skill.name }} {% if skill.situation %} ✧ {{ skill.situation }} {% endif %}

{% endfor %}
{% else %}
- Не указаны
{% endif %}
            """
        ),
        Button(Const(CONFIRM_BTN_TXT), on_click=on_confirmation, id="confirm"),
        Cancel(Const("✖️ Удалить")),
        getter=get_confirmation_data,
        state=states.CreateDiaryCardSG.CONFIRMATION,
        parse_mode="HTML",
    ),
    getter=get_data,
)
