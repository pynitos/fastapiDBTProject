from collections.abc import AsyncIterable
from datetime import timedelta

from dishka import AnyOf, Provider, Scope, WithParents, decorate, from_context, provide, provide_all
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from src.diary_ms.application.admin.emotion.dto.emotion import GetEmotionAdminDTO, GetEmotionsAdminDTO
from src.diary_ms.application.admin.emotion.dto.mapper.emotion import EmotionAdminDTOMapper
from src.diary_ms.application.admin.emotion.interactors.commands.create_emotion import (
    CreateEmotionAdminHandler,
)
from src.diary_ms.application.admin.emotion.interactors.commands.delete import DeleteEmotionAdminHandler
from src.diary_ms.application.admin.emotion.interactors.commands.update import UpdateEmotionAdminHandler
from src.diary_ms.application.admin.emotion.interactors.queries.get_emotion import GetEmotionAdminHandler
from src.diary_ms.application.admin.emotion.interactors.queries.get_emotions import (
    GetEmotionsAdminHandler,
)
from src.diary_ms.application.admin.emotion.interfaces.gateway import (
    EmotionAdminDeleter,
    EmotionAdminReader,
    EmotionAdminSaver,
    EmotionAdminUpdater,
)
from src.diary_ms.application.common.interfaces.dispatcher.resolver import Resolver
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.diary_card import GetOwnDiaryCardDTO, GetOwnDiaryCardsDTO
from src.diary_ms.application.diary_card.dto.for_update_diary_card import GetDiaryCardForUpdateDTO
from src.diary_ms.application.diary_card.dto.mappers.diary_card import DiaryCardDTOMapperImpl
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
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
)
from src.diary_ms.application.dispatcher import DishkaResolver, DispatcherImpl, RegistryImpl
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardCommand
from src.diary_ms.domain.model.commands.emotion.create_emotion import CreateEmotionAdminCommand
from src.diary_ms.domain.model.commands.emotion.delete_emotion import DeleteEmotionAdminCommand
from src.diary_ms.domain.model.commands.emotion.update_emotion import UpdateEmotionAdminCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.infrastructure.auth.token import JwtTokenProcessor
from src.diary_ms.infrastructure.brokers.broker import BrokerImpl
from src.diary_ms.infrastructure.brokers.interface import Broker
from src.diary_ms.infrastructure.gateways.sqla.admin.emotion import EmotionAdminGateway
from src.diary_ms.infrastructure.gateways.sqla.db.session import new_session_maker
from src.diary_ms.infrastructure.gateways.sqla.diary_card import DiaryCardGateway
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

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, TransactionManager]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_broker_client(self, config: Settings) -> KafkaBroker:
        return KafkaBroker(config.BROKER_URI)

    @decorate
    async def get_broker_session(self, broker_client: KafkaBroker) -> AsyncIterable[KafkaBroker]:
        async with broker_client as broker:
            yield broker

    @provide(scope=Scope.REQUEST)
    async def get_broker(self, broker_session: KafkaBroker) -> AnyOf[BrokerImpl, Broker]:
        return BrokerImpl(broker_session=broker_session)

    @provide
    def get_diary_cards_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        DiaryCardGateway,
        DiaryCardReader,
        DiaryCardDTOForUpdateReader,
        DiaryCardSaver,
        DiaryCardUpdater,
        DiaryCardDeleter,
    ]:
        return DiaryCardGateway(db_model=DiaryCard, session=session)

    @provide
    def get_emotion_admin_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        EmotionAdminGateway,
        EmotionAdminReader,
        EmotionAdminSaver,
        EmotionAdminUpdater,
        EmotionAdminDeleter,
    ]:
        return EmotionAdminGateway(db_model=Emotion, session=session)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    mappers = provide_all(
        EmotionAdminDTOMapper,
        WithParents[DiaryCardDTOMapperImpl],
    )

    command_handlers = provide_all(
        CreateDiaryCard,
        UpdateDiaryCard,
        DeleteDiaryCard,
        CreateEmotionAdminHandler,
        UpdateEmotionAdminHandler,
        DeleteEmotionAdminHandler,
    )

    query_handlers = provide_all(
        GetOwnDiaryCards,
        GetOwnDiaryCard,
        GetDiaryCardForUpdate,
        GetEmotionsAdminHandler,
        GetEmotionAdminHandler,
    )

    event_handlers = provide_all(DiaryCardCreatedEventHandler, scope=Scope.REQUEST)

    dispather = provide(WithParents[DispatcherImpl], scope=Scope.REQUEST)
    resolver = provide(DishkaResolver, provides=Resolver, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def init_registry(self) -> RegistryImpl:
        registry = RegistryImpl()
        # Diary cards
        registry.register_command_handler(CreateDiaryCardCommand, CreateDiaryCard)
        registry.register_command_handler(UpdateDiaryCardCommand, UpdateDiaryCard)
        registry.register_command_handler(DeleteDiaryCardCommand, DeleteDiaryCard)

        registry.register_query_handler(GetOwnDiaryCardDTO, GetOwnDiaryCard)
        registry.register_query_handler(GetOwnDiaryCardsDTO, GetOwnDiaryCards)
        registry.register_query_handler(GetDiaryCardForUpdateDTO, GetDiaryCardForUpdate)

        registry.register_event_handler(DiaryCardCreatedEvent, DiaryCardCreatedEventHandler)
        # Emotions
        registry.register_command_handler(CreateEmotionAdminCommand, CreateEmotionAdminHandler)
        registry.register_command_handler(UpdateEmotionAdminCommand, UpdateEmotionAdminHandler)
        registry.register_command_handler(DeleteEmotionAdminCommand, DeleteEmotionAdminHandler)

        registry.register_query_handler(GetEmotionsAdminDTO, GetEmotionsAdminHandler)
        registry.register_query_handler(GetEmotionAdminDTO, GetEmotionAdminHandler)

        return registry
