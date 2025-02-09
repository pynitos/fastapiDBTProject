from dishka import FromDishka
from fastapi import Depends

from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.presentation.api.dependencies.security import security

TokenDep = Depends(security)

SenderDep = FromDishka[Sender]
