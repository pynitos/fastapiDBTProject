from collections.abc import AsyncIterable
from datetime import timedelta

from dishka import AnyOf, Provider, Scope, decorate, from_context, provide, provide_all
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from src.diary_ms.application.common.interfaces.mediator.base import Mediator
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.application.diary_card.interactors.commands.create_diary_card import (
    CreateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.delete_diary_card import (
    DeleteDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.update_diary_card import (
    UpdateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.events.diary_card_created import (
    DiaryCardCreatedEventHandler,
)
from src.diary_ms.application.diary_card.interactors.queries.get_diary_card_for_update import (
    GetDiaryCardForUpdate,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_card import (
    GetOwnDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_cards import (
    GetOwnDiaryCards,
)
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardDTOForUpdateReader,
    DiaryCardDTOReader,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.infrastructure.auth.token import JwtTokenProcessor
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

    @provide(scope=Scope.APP)
    def get_jwt_token_processor(self, config: Settings) -> JwtTokenProcessor:
        return JwtTokenProcessor(
            secret=config.JWT_SECRET_KEY,
            expires=timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            algorithm=config.JWT_ALGORITHM,
        )

    @provide
    def get_diary_cards_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        DiaryCardGateway,
        DiaryCardReader,
        DiaryCardDTOReader,
        DiaryCardDTOForUpdateReader,
        DiaryCardSaver,
        DiaryCardUpdater,
        DiaryCardDeleter,
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
