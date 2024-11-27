from abc import ABC, abstractmethod
from uuid import UUID

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.diary_ms.application.common.interfaces.gateway import (
    DeleterProtocol,
    DTOForUpdateReader,
    DTOReader,
    ReaderProtocol,
    SaverProtocol,
    UpdaterProtocol,
)
from src.diary_ms.application.common.interfaces.uow import UOWProtocol


class BaseGateway[
    TDModel,
    TModel: SQLModel,
](
    ABC,
    ReaderProtocol,
    SaverProtocol,
    DeleterProtocol,
    UpdaterProtocol,
    DTOReader,
    DTOForUpdateReader,
):
    def __init__(
        self,
        db_model: TModel,
        domain_model: type[TDModel],
        session: AsyncSession | UOWProtocol,
    ) -> None:
        self._session = session
        self._db_model = db_model
        self._domain_model = domain_model

    @abstractmethod
    async def get_by_id(self, pk: UUID) -> TDModel | None:
        pass

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[TDModel]:
        pass

    @abstractmethod
    async def create(self, entity: TDModel) -> None:
        pass

    @abstractmethod
    async def update(
        self,
        pk: UUID,
        entity: TModel,
    ) -> TModel:
        pass

    @abstractmethod
    async def delete(self, entity: TModel) -> None:
        pass
