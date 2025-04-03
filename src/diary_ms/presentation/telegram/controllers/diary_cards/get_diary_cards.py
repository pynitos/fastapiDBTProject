from dataclasses import asdict
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Column, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.application.diary_card.dto.diary_card import GetOwnDiaryCardDTO, GetOwnDiaryCardsDTO
from src.diary_ms.presentation.telegram.common.constants.mood import MoodDisplay

from . import states


async def on_card_selected(_: CallbackQuery, __: Select, manager: DialogManager, item_id: str):
    manager.dialog_data["selected_card_id"] = item_id
    await manager.switch_to(states.GetOwnDiaryCardsSG.detail_view)


async def on_delete_clicked(_: CallbackQuery, __: Button, manager: DialogManager):
    await manager.switch_to(states.GetOwnDiaryCardsSG.confirm_delete)


@inject
async def on_delete_confirmed(callback: CallbackQuery, _: Button, manager: DialogManager, sender: FromDishka[Sender]):
    diary_card_id = manager.dialog_data["selected_card_id"]
    await sender.send_command(DeleteDiaryCardCommand(id=diary_card_id))
    await callback.answer("Запись удалена!")
    await manager.done()


@inject
async def get_cards_list(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs) -> dict[str, Any]:
    diary_cards = await sender.send_query(GetOwnDiaryCardsDTO(Pagination(10, 0)))
    return {"diary_cards": diary_cards}


@inject
async def get_card_details(dialog_manager: DialogManager, sender: FromDishka[Sender], **kwargs) -> dict[str, Any]:
    card_id = dialog_manager.dialog_data["selected_card_id"]
    card = await sender.send_query(GetOwnDiaryCardDTO(id=card_id))
    mood = MoodDisplay.from_level(card.mood)
    return {
        "item": {**asdict(card), "mood_emoji": mood.emoji, "mood_text": mood.text, "date_of_entry": card.date_of_entry}
    }


list_window = Window(
    Const("📅 Ваши дневниковые записи:"),
    ScrollingGroup(
        Select(
            Format("{item.date_of_entry:%d.%m.%Y} ⭐ {item.mood}/5"),
            id="s_cards",
            item_id_getter=lambda x: str(x.id),
            items="diary_cards",
            on_click=on_card_selected,
        ),
        id="scroll_cards",
        width=1,
        height=5,
    ),
    Cancel(Const("◀️ Назад")),
    state=states.GetOwnDiaryCardsSG.view,
    getter=get_cards_list,
)

# Детали карточки
detail_window = Window(
    Jinja(
        """
📅 <b>{{ item.date_of_entry.strftime('%d.%m.%Y') }}</b>
<b>Настроение:</b> {{ item.mood_text }} {{ item.mood_emoji }}
{% if item.description %}
📝 <b>Описание:</b>
{{ item.description }}
{% endif %}
{% if item.targets %}
🎯 <b>Целевое поведение:</b>
{% for target in item.targets %}
• {{ target.urge }}
  {% if target.action %}→ {{ target.action }}{% endif %}
  {% if target.effectiveness %} ⭐ {{ target.effectiveness }}/10{% endif %}

{% endfor %}
{% endif %}
"""
    ),
    Column(Button(Const("❌ Удалить"), id="btn_delete", on_click=on_delete_clicked), Back(Const("◀️ К списку"))),
    state=states.GetOwnDiaryCardsSG.detail_view,
    getter=get_card_details,
    parse_mode="HTML",
)

# Подтверждение удаления
confirm_delete_window = Window(
    Const("Вы уверены, что хотите удалить эту запись?"),
    Column(
        Button(Const("✅ Да, удалить"), id="btn_confirm_delete", on_click=on_delete_confirmed), Back(Const("◀️ Отмена"))
    ),
    state=states.GetOwnDiaryCardsSG.confirm_delete,
)

own_diary_cards_dialog = Dialog(
    list_window,
    detail_window,
    confirm_delete_window,
)
