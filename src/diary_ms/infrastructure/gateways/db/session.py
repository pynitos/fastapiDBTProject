from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.diary_ms.main.config import Settings


def new_session_maker(settings: Settings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
