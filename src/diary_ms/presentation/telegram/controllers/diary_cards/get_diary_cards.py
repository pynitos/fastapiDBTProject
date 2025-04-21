from dataclasses import asdict
from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Column, Group, NumberedPager, Select, StubScroll
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.dto.pagination import PAGE_SIZE, Pagination
from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardQuery,
    GetOwnDiaryCardsQuery,
    OwnDiaryCardResultDTO,
    OwnDiaryCardsResultDTO,
)
from src.diary_ms.presentation.telegram.common.constants import BACK_BTN_TXT, CANCEL_BTN_TXT, REMOVE_BTN_TXT
from src.diary_ms.presentation.telegram.common.constants.mood import MoodDisplay

from . import states


async def on_card_selected(_: CallbackQuery, __: Select[str], manager: DialogManager, item_id: str) -> None:
    manager.dialog_data["selected_card_id"] = item_id
    await manager.switch_to(states.GetOwnDiaryCardsSG.detail_view)


async def on_delete_clicked(_: CallbackQuery, __: Button, manager: DialogManager) -> None:
    await manager.switch_to(states.GetOwnDiaryCardsSG.confirm_delete)


@inject
async def on_delete_confirmed(
    callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]
) -> None:
    diary_card_id = manager.dialog_data["selected_card_id"]
    await sender.send_command(DeleteDiaryCardCommand(id=diary_card_id))
    await callback.answer("Запись удалена!")
    await manager.done()


@inject
async def get_diary_cards(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs: Any) -> dict[str, Any]:  # noqa: ARG001
    scroll: ManagedScroll | None = dialog_manager.find("scroll_diary_cards")
    page: int = await scroll.get_page() if scroll else 1
    offset: int = page * PAGE_SIZE
    result: OwnDiaryCardsResultDTO = await sender.send_query(GetOwnDiaryCardsQuery(Pagination(PAGE_SIZE, offset)))
    return {
        "diary_cards": result.diary_cards,
        "total": result.total,
        "pages": result.total // PAGE_SIZE + bool(result.total % PAGE_SIZE),
    }


@inject
async def get_diary_card_details(
    dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs: Any
) -> dict[str, Any]:  # noqa: ARG001
    card_id = dialog_manager.dialog_data["selected_card_id"]
    card: OwnDiaryCardResultDTO = await sender.send_query(GetOwnDiaryCardQuery(id=card_id))
    mood = MoodDisplay.from_level(card.mood)
    return {
        "item": {**asdict(card), "mood_emoji": mood.emoji, "mood_text": mood.text, "date_of_entry": card.date_of_entry}
    }


list_window = Window(
    Format("📅 Ваши дневниковые карточки ({total}):", when=F["total"]),
    Const("📅 У Вас нет дневниковых карточек:", when=~F["total"]),
    StubScroll(id="scroll_diary_cards", pages=F["pages"]),
    Column(
        Select(
            Format("{item.date_of_entry:%d.%m.%Y} ⭐ {item.mood}/5"),
            id="s_cards",
            item_id_getter=lambda x: str(x.id),
            items="diary_cards",
            on_click=on_card_selected,
        ),
    ),
    Group(
        NumberedPager(id="pager_diary_cards", scroll="scroll_diary_cards"),
        width=8,
    ),
    Cancel(Const(BACK_BTN_TXT)),
    state=states.GetOwnDiaryCardsSG.view,
    getter=get_diary_cards,
)

# Детали карточки
detail_window = Window(
    Jinja(
        """
📅 <b>{{ item.date_of_entry.strftime('%d.%m.%Y') }}</b>

🌡 <b>Настроение:</b> {{ item.mood_emoji }} ({{ item.mood_text }})
{% if item.description %}

📄 <b>Описание дня:</b>
{{ item.description }}
{% endif %}

🎯 <b>Целевое поведение:</b>
{% if item.targets %}
{% for target in item.targets -%}
▸ {{ target.urge }}{% if target.action %}: <i>{{ target.action }}</i>\n{% endif %}
{% if target.effectiveness %}↳ Эффективность: <i>{{ target.effectiveness }}/10</i>{% endif %}\n
{% endfor %}
{% else %}
▹ <i>не указано</i>
{% endif %}

🌊 <b>Эмоции:</b>
{% if item.emotions %}
{% for emotion in item.emotions -%}
▸ {{ emotion.name }}
{% endfor %}
{% else %}
▹ <i>не указано</i>
{% endif %}

💊 <b>Медикаменты:</b>
{% if item.medicaments %}
{% for med in item.medicaments -%}
▸ {{ med.name }} (<code>{{ med.dosage }}</code>)
{% endfor %}
{% else %}
▸ <i>не указаны</i>
{% endif %}

🛠️ <b>Применённые навыки:</b>
{% if item.skills %}
{% for skill in item.skills -%}
▸ {{ skill.name }}{% if skill.usage %}: <i>{{ skill.usage }}</i>
{% endif %}
{% if skill.effectiveness %}↳ Эффективность: <i>{{ skill.effectiveness }}/7</i>
{% endif %}
{% endfor %}
{% else %}
▹ <i>не указано</i>
{% endif %}
"""
    ),
    Column(Button(Const(REMOVE_BTN_TXT), id="btn_delete", on_click=on_delete_clicked), Back(Const("◀️ К списку"))),
    state=states.GetOwnDiaryCardsSG.detail_view,
    getter=get_diary_card_details,
    parse_mode="HTML",
)

# Подтверждение удаления
confirm_delete_window = Window(
    Const("Вы уверены, что хотите удалить эту запись?"),
    Column(
        Button(Const("✅ Да, удалить"), id="btn_confirm_delete", on_click=on_delete_confirmed),
        Back(Const(CANCEL_BTN_TXT)),
    ),
    state=states.GetOwnDiaryCardsSG.confirm_delete,
)

own_diary_cards_dialog = Dialog(
    list_window,
    detail_window,
    confirm_delete_window,
)
