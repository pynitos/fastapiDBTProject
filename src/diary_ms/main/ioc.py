from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, decorate, from_context, provide, provide_all
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.interfaces.diary_card import (
    DeleterProtocol,
    DTOForUpdateReader,
    DTOReader,
    ReaderProtocol,
    SaverProtocol,
    UpdaterProtocol,
)
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.mediator.base import Mediator
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.application.interactors.commands.create_diary_card import (
    CreateDiaryCard,
)
from src.diary_ms.application.interactors.commands.delete_diary_card import (
    DeleteDiaryCard,
)
from src.diary_ms.application.interactors.commands.update_diary_card import (
    UpdateDiaryCard,
)
from src.diary_ms.application.interactors.events.diary_card_created import (
    DiaryCardCreatedEventHandler,
)
from src.diary_ms.application.interactors.queries.get_diary_card_for_update import (
    GetDiaryCardForUpdate,
)
from src.diary_ms.application.interactors.queries.get_own_diary_card import (
    GetOwnDiaryCard,
)
from src.diary_ms.application.interactors.queries.get_own_diary_cards import (
    GetOwnDiaryCards,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.infrastructure.auth.token import FakeIdProvider
from src.diary_ms.infrastructure.brokers.broker import BrokerImpl
from src.diary_ms.infrastructure.brokers.interface import Broker
from src.diary_ms.infrastructure.gateways.db.session import new_session_maker
from src.diary_ms.infrastructure.gateways.diary_card import DiaryCardGateway
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard
from src.diary_ms.infrastructure.mediator.base import init_mediator
from src.diary_ms.main.config import Settings


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(provides=Settings, scope=Scope.APP)
    id_provider = provide(FakeIdProvider, provides=IdProvider)

    @provide
    def get_diary_cards_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        DiaryCardGateway,
        ReaderProtocol,
        DTOReader,
        DTOForUpdateReader,
        SaverProtocol,
        UpdaterProtocol,
        DeleterProtocol,
    ]:
        return DiaryCardGateway(
            db_model=DiaryCard, domain_model=DiaryCardDM, session=session
        )

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, UOWProtocol]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_broker_client(self, config: Settings) -> KafkaBroker:
        return KafkaBroker(config.BROKER_URI)

    @decorate
    async def get_broker_session(
        self, broker_client: KafkaBroker
    ) -> AsyncIterable[KafkaBroker]:
        async with broker_client as broker:
            yield broker

    @provide(scope=Scope.REQUEST)
    async def get_broker(
        self, broker_session: KafkaBroker
    ) -> AnyOf[BrokerImpl, Broker]:
        return BrokerImpl(broker_session=broker_session)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    command_handlers = provide_all(
        CreateDiaryCard,
        UpdateDiaryCard,
        DeleteDiaryCard,
    )

    query_handlers = provide_all(
        GetOwnDiaryCards,
        GetOwnDiaryCard,
        GetDiaryCardForUpdate,
    )

    event_handlers = provide_all(
        DiaryCardCreatedEventHandler,
    )

    mediator = provide(init_mediator, provides=Mediator)
