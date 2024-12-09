from src.diary_ms.application.common.interfaces.handlers.command import (
    CT,
    CommandHandler,
)
from src.diary_ms.application.common.interfaces.handlers.event import ET, EventListener
from src.diary_ms.application.common.interfaces.handlers.query import QT, QueryHandler
from src.diary_ms.domain.common.model.events.base import BaseEvent


# class MediatorImpl:
#     def __init__(self):
#         self.command_handlers: dict[CT, CommandHandler] = {}
#         self.query_handlers: dict[QT, QueryHandler[QT, QR]] = {}
#         self.event_listeners: list[EventListener[BaseEvent]] = []
