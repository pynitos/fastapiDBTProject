from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Start
from aiogram_dialog.widgets.text import Const

from src.diary_ms.presentation.telegram.controllers.medicaments.states import GetOwnMedicamentsSG
from src.diary_ms.presentation.telegram.controllers.states import MainMenuSG
from src.diary_ms.presentation.telegram.controllers.targets.states import GetTargetsSG

from .diary_cards.states import CreateDiaryCardSG, GetOwnDiaryCardsSG

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
            Start(
                Const("🎯 Целевое поведение"),
                id="manage_targets",
                state=GetTargetsSG.view,
            ),
        ),
        state=MainMenuSG.main,
        parse_mode="HTML",
    )
)
