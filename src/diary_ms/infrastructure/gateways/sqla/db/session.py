from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from diary_ms.infrastructure.gateways.sqla.db.mapper import init_mapper
from diary_ms.main.config import WebConfig


def new_session_maker(config: WebConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        str(config.DB_URI),
        pool_size=15,
        max_overflow=15,
        connect_args={
            "command_timeout": 5,
        },
    )
    init_mapper()
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
