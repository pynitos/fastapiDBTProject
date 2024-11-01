from dishka import FromDishka

from app.diary_ms.application.interactors.diary_card.get_dc import GetOwnDiaryCards
from app.diary_ms.core.config import Settings

SettingsDep = FromDishka[Settings]
GetOwnDiaryCardsDep = FromDishka[GetOwnDiaryCards]
