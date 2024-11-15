from typing import AsyncIterable

from dishka import Scope, Provider, provide, from_context, AnyOf
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.diary_ms.application.interactors.commands.create_diary_card import CreateDiaryCard
from src.diary_ms.application.interactors.queries.get_own_diary_cards import GetOwnDiaryCards
from src.diary_ms.application.interfaces.gateway import ReaderProtocol, SaverProtocol
from src.diary_ms.application.interfaces.id_provider import IdProvider
from src.diary_ms.application.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.infrastructure.auth.token import FakeIdProvider
from src.diary_ms.infrastructure.gateways.db.session import new_session_maker
from src.diary_ms.infrastructure.gateways.diary_card import DiaryCardGateway
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard
from src.diary_ms.main.config import Settings


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(provides=Settings, scope=Scope.APP)
    id_provider = provide(FakeIdProvider, provides=IdProvider)

    @provide
    def get_diary_cards_gateway(self, session: AsyncSession) -> AnyOf[DiaryCardGateway, ReaderProtocol, SaverProtocol]:
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
    create_diary_card = provide(CreateDiaryCard)
