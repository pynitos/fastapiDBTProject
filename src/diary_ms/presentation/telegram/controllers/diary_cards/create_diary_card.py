import logging
import operator
from dataclasses import asdict
from typing import Any

from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Group,
    ManagedMultiselect,
    Multiselect,
    Next,
    Row,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject
from magic_filter import F

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import (
    CreateCopingStrategyCommand,
    CreateDiaryCardCommand,
    CreateSkillApplicationCommand,
)
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery
from src.diary_ms.presentation.telegram.common.constants import (
    ADD_BTN_TXT,
    BACK_BTN_TXT,
    CANCEL_BTN_TXT,
    CONFIRM_BTN_TXT,
    NEXT_BTN_TXT,
    REMOVE_BTN_TXT,
)
from src.diary_ms.presentation.telegram.common.constants.mood import MoodDisplay
from src.diary_ms.presentation.telegram.controllers.medicaments.states import CreateMedicamentSG

from . import states

logger = logging.getLogger(__name__)


async def on_mood_selected(_: CallbackQuery, __: Select[int], manager: DialogManager, selected: int) -> None:
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
async def get_data(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
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
    dialog_manager.dialog_data["medicaments"] = medicaments

    return {
        "moods": moods,
        "emotions": emotions,
        "skills": skills,
        "targets": targets,
        "medicaments": medicaments,
    }


async def on_target_selected(
    _: CallbackQuery,
    select: ManagedMultiselect[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    if not select.is_checked(data):
        dialog_manager.dialog_data["current_target"] = [
            t for t in dialog_manager.dialog_data["targets"] if str(t["id"]) == data
        ][0]
        await dialog_manager.next()
    else:
        targets = dialog_manager.dialog_data.setdefault("targets_for_confirm", [])
        dialog_manager.dialog_data["targets_for_confirm"] = [t for t in targets if t["id"] != data]
        await dialog_manager.switch_to(states.CreateDiaryCardSG.targets)


async def on_targets_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data.setdefault("targets_for_confirm", [])
    await dialog_manager.switch_to(states.CreateDiaryCardSG.target_effectiveness)


async def target_name_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
    current_target = dialog_manager.dialog_data["current_target"]
    return {"target_name": current_target["urge"]}


async def on_target_action_entered(
    message: Message,
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    action: str,
) -> None:
    current_target = dialog_manager.dialog_data["current_target"]
    current_target["action"] = action  # Сохраняем action для текущей цели
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()
    await dialog_manager.next()


async def on_target_effectiveness_selected(
    _: CallbackQuery,
    __: Select[int],
    dialog_manager: DialogManager,
    selected: int,
) -> None:
    current_target = dialog_manager.dialog_data["current_target"]
    current_target["effectiveness"] = selected
    dialog_manager.dialog_data.setdefault("targets_for_confirm", []).append(current_target)
    await dialog_manager.switch_to(states.CreateDiaryCardSG.targets)


async def on_target_action_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    current_target = dialog_manager.dialog_data["current_target"]
    current_target["action"] = None
    dialog_manager.dialog_data.setdefault("targets_for_confirm", []).append(current_target)
    await dialog_manager.switch_to(states.CreateDiaryCardSG.targets)


async def on_target_effectiveness_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    current_target = dialog_manager.dialog_data["current_target"]
    dialog_manager.dialog_data.setdefault("targets_for_confirm", []).append(current_target)
    await dialog_manager.switch_to(states.CreateDiaryCardSG.targets)


async def on_skills_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data.setdefault("skills_for_confirm", [])
    await dialog_manager.switch_to(states.CreateDiaryCardSG.skill_effectiveness)


async def skill_name_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
    current_skill = dialog_manager.dialog_data["current_skill"]
    return {"skill_name": current_skill["name"]}


async def on_skill_selected(
    _: CallbackQuery,
    select: ManagedMultiselect[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    if not select.is_checked(data):
        dialog_manager.dialog_data["current_skill"] = [
            s for s in dialog_manager.dialog_data["skills"] if str(s["id"]) == data
        ][0]
        await dialog_manager.next()
    else:
        skills = dialog_manager.dialog_data.setdefault("skills_for_confirm", [])
        dialog_manager.dialog_data["targets_for_confirm"] = [t for t in skills if t["id"] != data]
        await dialog_manager.switch_to(states.CreateDiaryCardSG.skills)


async def on_skill_usage_entered(
    message: Message,
    _: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    current_skill = dialog_manager.dialog_data["current_skill"]
    current_skill["usage"] = data
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()
    await dialog_manager.next()


async def on_skill_usage_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    current_skill = dialog_manager.dialog_data["current_skill"]
    current_skill["usage"] = None
    dialog_manager.dialog_data.setdefault("skills_for_confirm", []).append(current_skill)
    await dialog_manager.switch_to(states.CreateDiaryCardSG.skills)


async def on_skill_effectiveness_selected(
    _: CallbackQuery,
    __: Select[int],
    dialog_manager: DialogManager,
    selected: int,
) -> None:
    current_skill = dialog_manager.dialog_data["current_skill"]
    current_skill["effectiveness"] = selected
    dialog_manager.dialog_data.setdefault("skills_for_confirm", []).append(current_skill)
    await dialog_manager.switch_to(states.CreateDiaryCardSG.skills)


async def on_skill_effectiveness_next_btn(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    current_skill = dialog_manager.dialog_data["current_skill"]
    dialog_manager.dialog_data.setdefault("skills_for_confirm", []).append(current_skill)
    await dialog_manager.switch_to(states.CreateDiaryCardSG.skills)


async def get_confirmation_data(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
    # Преобразуем число в текстовое описание для отображения
    mood_mapping = {
        1: "Очень плохое",
        2: "Плохое",
        3: "Нейтральное",
        4: "Хорошее",
        5: "Отличное",
    }
    mood = MoodDisplay.from_level(dialog_manager.dialog_data.get("mood", "Не указано"))
    ms_emotions = dialog_manager.find("ms_emotions")
    e_ids = ms_emotions.get_checked() if ms_emotions else []
    emotions = [e for e in dialog_manager.dialog_data["emotions"] if str(e["id"]) in e_ids]
    ms_medicaments = dialog_manager.find("ms_medicaments")
    m_ids = ms_medicaments.get_checked() if ms_medicaments else []
    medicaments = [m for m in dialog_manager.dialog_data["medicaments"] if str(m["id"]) in m_ids]
    skills = dialog_manager.dialog_data.get("skills_for_confirm", [])
    targets = dialog_manager.dialog_data.get("targets_for_confirm", [])
    return {
        "mood": mood.text,
        "description": dialog_manager.dialog_data.get("description", "Не указано"),
        "target_copings": targets,
        "emotions": emotions,
        "medicaments": medicaments,
        "skills": skills,
    }


@inject
async def on_confirmation(
    callback: CallbackQuery, __: Button, dialog_manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    ms_emotions = dialog_manager.find("ms_emotions")
    emotions_ids = ms_emotions.get_checked() if ms_emotions else []
    ms_medicaments = dialog_manager.find("ms_medicaments")
    medicaments_ids = ms_medicaments.get_checked() if ms_medicaments else []
    skills = dialog_manager.dialog_data.get("skills_for_confirm", [])
    skills_for_create = [
        CreateSkillApplicationCommand(id=s["id"], skill_usage=s.get("usage"), effectiveness=s.get("effectiveness"))
        for s in skills
    ]
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
            medicaments=medicaments_ids,
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
        Const("Опишите ваш день:"),
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
                on_click=on_target_selected,
            )
        ),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_targets_next_btn)),
        state=states.CreateDiaryCardSG.targets,
    ),
    Window(
        Format("📌  <b>Проблемное поведение:</b> {target_name}.\n\nОпишите ситуацию и применённые навыки:"),
        TextInput(id="target_action_input", on_success=on_target_action_entered),
        Row(
            Back(Const(BACK_BTN_TXT)),
            Button(Const(NEXT_BTN_TXT), id="target_action_next_btn", on_click=on_target_action_next_btn),
        ),
        state=states.CreateDiaryCardSG.target_action,
        getter=target_name_getter,
        parse_mode="HTML",
    ),
    Window(
        Format("📌 <b>Проблемное поведение:</b> {target_name}\n\nОцените эффективность применения навыков"),
        Group(
            Select(
                Format("{item}"),
                id="select_effectiveness",
                items=list(range(0, 8)),  # Числа от 0 до 7
                item_id_getter=lambda x: x,
                on_click=on_target_effectiveness_selected,
                type_factory=int,
            ),
            width=4,
        ),
        Row(
            Back(Const(BACK_BTN_TXT)),
            Button(Const(NEXT_BTN_TXT), id="target_eff_next_btn", on_click=on_target_effectiveness_next_btn),
        ),
        state=states.CreateDiaryCardSG.target_effectiveness,
        getter=target_name_getter,
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
                Format("✓ {item[name]} ({item[dosage]})"),
                Format("{item[name]} | {item[dosage]}"),
                id="ms_medicaments",
                item_id_getter=lambda x: str(x["id"]),
                items="medicaments",
            ),
        ),
        Start(Const(ADD_BTN_TXT), id="add_medicament", state=CreateMedicamentSG.name, when=~F["medicaments"]),
        Row(
            SwitchTo(Const(BACK_BTN_TXT), id="back_to_targets", state=states.CreateDiaryCardSG.targets),
            Next(Const(NEXT_BTN_TXT)),
        ),
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
                on_click=on_skill_selected,
            )
        ),
        Row(Back(Const(BACK_BTN_TXT)), Next(Const(NEXT_BTN_TXT), on_click=on_skills_next_btn)),
        state=states.CreateDiaryCardSG.skills,
    ),
    Window(
        Format("Опишите то, как вы применили навык: {skill_name}"),
        Row(
            Back(Const(BACK_BTN_TXT)),
            Button(Const(NEXT_BTN_TXT), id="skill_usage_next_btn", on_click=on_skill_usage_next_btn),
        ),
        TextInput[str](id="skill_input_id", on_success=on_skill_usage_entered),
        state=states.CreateDiaryCardSG.skill_usage,
        getter=skill_name_getter,
    ),
    Window(
        Format("📌 Оцените эффективность применения навыка {skill_name}"),
        Group(
            Select(
                Format("{item}"),
                id="select_skill_effectiveness",
                items=list(range(0, 8)),  # Числа от 0 до 7
                item_id_getter=lambda x: x,
                on_click=on_skill_effectiveness_selected,
                type_factory=int,
            ),
            width=4,
        ),
        Row(
            Back(Const(BACK_BTN_TXT)),
            Button(Const(NEXT_BTN_TXT), id="skill_eff_next_btn", on_click=on_skill_effectiveness_next_btn),
        ),
        state=states.CreateDiaryCardSG.skill_effectiveness,
        getter=skill_name_getter,
        parse_mode="HTML",
    ),
    Window(
        Jinja(
            """
<b>📋 Проверьте введенные данные:</b>

<b>Настроение:</b> {{ mood }}

{% if description %}
<b>Описание:</b> {{ description }}

{% endif %}
<b>🎯 Проблемное поведение:</b>
{% if target_copings %}
{% for t in target_copings -%}
• {{ t.urge }} {% if t.action %}
✧ {{ t.action }}{% if t.effectiveness %} | {{ t.effectiveness }}/7{% endif %}
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
• {{ med.name }}
{% endfor %}
{% else %}
- Не указаны
{% endif %}
<b>🛠 Навыки:</b>
{% if skills %}
{% for s in skills -%}
• {{ s.name }} {% if s.usage %}
✧ {{ s.usage }}{% if s.effectiveness %} | {{ s.effectiveness }}/7{% endif %}
{% endif %}

{% endfor %}
{% else %}
- Не указаны
{% endif %}
            """
        ),
        Button(Const(CONFIRM_BTN_TXT), on_click=on_confirmation, id="confirm"),
        Cancel(Const(REMOVE_BTN_TXT)),
        getter=get_confirmation_data,
        state=states.CreateDiaryCardSG.CONFIRMATION,
        parse_mode="HTML",
    ),
    getter=get_data,
)
