from typing import AsyncIterable

from dishka import Scope, Provider, provide, from_context, AnyOf
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.diary_ms.adapters.db.session import new_session_maker
from app.diary_ms.adapters.gateways.diary_card import DiaryCardGateway
from app.diary_ms.adapters.models.diary_card import DiaryCard
from app.diary_ms.application.interactors.diary_card.get_dc import GetOwnDiaryCards
from app.diary_ms.application.interfaces.gateway import ReaderProtocol
from app.diary_ms.application.interfaces.uow import UOWProtocol
from app.diary_ms.core.config import Settings
from app.diary_ms.domain.models.diary_card import DiaryCardDM


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide
    def get_diary_cards_gateway(self, session: AsyncSession) -> AnyOf[DiaryCardGateway, ReaderProtocol]:
        return DiaryCardGateway(db_model=DiaryCard, domain_model=DiaryCardDM, session=session)

    @provide(scope=Scope.APP)
    def get_session_maker(self, settings: Settings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(settings)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[
        AnyOf[AsyncSession, UOWProtocol]
    ]:
        async with session_maker() as session:
            yield session


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    own_diary_cards = provide(GetOwnDiaryCards)
