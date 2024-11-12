from dishka import FromDishka

from src.diary_ms.application.interactors.queries.get_own_diary_cards import GetOwnDiaryCards
from src.diary_ms.main.config import Settings

SettingsDep = FromDishka[Settings]
GetOwnDiaryCardsDep = FromDishka[GetOwnDiaryCards]

GetDiaryCardDep = FromDishka[GetOwnDiaryCards]
