from dishka import FromDishka

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender

AMQPSenderDep = FromDishka[Sender]
