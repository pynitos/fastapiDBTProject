from aiogram_dialog.widgets.kbd import Back, Next, Row
from aiogram_dialog.widgets.text import Const
from magic_filter import MagicFilter

from diary_ms.presentation.telegram.common.constants import BACK_BTN_TXT, NEXT_BTN_TXT


def back_next_row(
    back_btn_txt: str = BACK_BTN_TXT, next_btn_txt: str = NEXT_BTN_TXT, when: str | MagicFilter | None = None
) -> Row:
    return Row(Back(Const(back_btn_txt)), Next(Const(next_btn_txt)), when=when)
