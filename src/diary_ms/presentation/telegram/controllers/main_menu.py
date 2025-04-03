from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const

from .diary_cards.states import CreateDiaryCardSG, GetOwnDiaryCardsSG


class MainMenuSG(StatesGroup):
    main = State()


async def on_manage_targets(callback: CallbackQuery, button: Button, manager: DialogManager):
    # await manager.start(ManageTargetsStates.menu)
    pass


main_menu_dialog = Dialog(
    Window(
        Const("📋 <b>Главное меню DBT-дневника:</b>"),
        Column(
            Button(
                Const("📝 Заполнить новую карточку"),
                id="create_card",
                on_click=lambda _, __, m: m.start(CreateDiaryCardSG.mood),
            ),
            Button(
                Const("📖 Мои дневниковые карточки"),
                id="view_cards",
                on_click=lambda _, __, m: m.start(GetOwnDiaryCardsSG.view),
            ),
            # Button(
            #     Const("💊 Медикаменты"),
            #     id="manage_meds",
            #     on_click=lambda _, __, m: m.start(ManageMedsStates.menu)
            # ),
            # Button(
            #     Const("🎯 Цели"),  # Изменил "Задачи" на "Цели"
            #     id="manage_targets",
            #     on_click=on_manage_targets
            # ),
        ),
        state=MainMenuSG.main,
        parse_mode="HTML",
    )
)
