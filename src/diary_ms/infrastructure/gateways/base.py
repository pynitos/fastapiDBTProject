from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.engine import TupleResult
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import select, SelectOfScalar

from src.diary_ms.application.interfaces.gateway import ReaderProtocol, SaverProtocol, UpdaterProtocol, DeleterProtocol
from src.diary_ms.application.interfaces.uow import UOWProtocol


class BaseGateway[TModel: SQLModel, TDModel](ReaderProtocol, SaverProtocol, UpdaterProtocol, DeleterProtocol):
    def __init__(self, db_model: TModel, domain_model: type[TDModel], session: AsyncSession | UOWProtocol) -> None:
        self._session = session
        self._db_model = db_model
        self._domain_model = domain_model

    async def get_by_id(self, pk: UUID) -> TDModel | None:
        entity: TDModel = await self._session.get(self._db_model, pk)
        return self._domain_model(**entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[TDModel]:
        stmt: SelectOfScalar = select(self._db_model).offset(offset).limit(limit)
        result: TupleResult = await self._session.exec(stmt)
        result_list: list[TModel] = result.all()
        domain_list: list[TDModel] = [self._domain_model(
            **x.model_dump(exclude={'created_at', 'updated_at'})
        ) for x in result_list]
        return domain_list

    async def create(self, entity: TDModel) -> None:
        db_entity: TModel = self._db_model.model_validate(entity)
        self._session.add(db_entity)

    async def update(
            self, pk: UUID, entity: TModel,
    ) -> TModel:
        db_entity = await self.get_by_id(pk)
        if not db_entity:
            raise HTTPException(status_code=404, detail="Not found.")
        entity_data = entity.model_dump(exclude_unset=True)
        db_entity.sqlmodel_update(entity_data)

        self._session.add(db_entity)
        await self._session.commit()
        await self._session.refresh(db_entity)
        return self._domain_model(**entity)

    async def delete(self, entity: TModel) -> None:
        await self._session.delete(entity)
        await self._session.commit()
