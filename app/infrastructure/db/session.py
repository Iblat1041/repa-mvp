from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Создать (или вернуть ранее созданный) движок SQLAlchemy."""
    global _engine  # noqa: PLW0603
    if _engine is None:
        _engine = create_async_engine(
            settings.db_url,
            echo=settings.echo_sql,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Вернуть фабрику асинхронных сессий."""
    global _session_factory  # noqa: PLW0603
    if _session_factory is None:
        _session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency FastAPI — выдаёт асинхронную сессию и закрывает её."""
    async_session = get_session_factory()
    async with async_session() as session:
        yield session