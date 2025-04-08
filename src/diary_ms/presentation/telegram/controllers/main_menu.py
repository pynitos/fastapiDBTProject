from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Start
from aiogram_dialog.widgets.text import Const

from src.diary_ms.presentation.telegram.controllers.medicaments.states import GetOwnMedicamentsSG

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
            Start(
                Const("📝 Заполнить новую карточку"),
                id="create_card",
                state=CreateDiaryCardSG.mood,
            ),
            Start(
                Const("📖 Мои дневниковые карточки"),
                id="view_cards",
                state=GetOwnDiaryCardsSG.view,
            ),
            Start(Const("💊 Медикаменты"), id="manage_meds", state=GetOwnMedicamentsSG.view),
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
