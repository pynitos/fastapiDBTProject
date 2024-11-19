from dishka import FromDishka

from src.diary_ms.application.interactors.commands.create_diary_card import CreateDiaryCard
from src.diary_ms.application.interactors.queries.get_own_diary_card import GetOwnDiaryCard
from src.diary_ms.application.interactors.queries.get_own_diary_cards import GetOwnDiaryCards

GetOwnDiaryCardsDep = FromDishka[GetOwnDiaryCards]
GetDiaryCardDep = FromDishka[GetOwnDiaryCard]
CreateDiaryCardDep = FromDishka[CreateDiaryCard]
