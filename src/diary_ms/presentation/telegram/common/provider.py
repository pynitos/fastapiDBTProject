import logging

from aiogram.types import TelegramObject
from dishka import AnyOf, Provider, Scope, from_context, provide

from diary_ms.application.common.interfaces.id_provider import (
    AdminIdProvider,
    IdProvider,
)
from diary_ms.infrastructure.auth.tg import TgIdProvider

logger = logging.getLogger(__name__)


class TgProvider(Provider):
    scope = Scope.REQUEST

    tg_object = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide
    def get_user_id_provider(
        self,
        obj: TelegramObject,
    ) -> AnyOf[IdProvider, AdminIdProvider, TgIdProvider]:
        tg_user_id: int = obj.from_user.id  # type: ignore
        return TgIdProvider(tg_user_id=tg_user_id)
