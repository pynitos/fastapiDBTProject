from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.infrastructure.gateways.sqla.db.mapper import init_mapper
from src.diary_ms.main.config import Settings


def new_session_maker(settings: Settings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        pool_size=15,
        max_overflow=15,
        connect_args={
            "command_timeout": 5,
        },
    )
    init_mapper()
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
