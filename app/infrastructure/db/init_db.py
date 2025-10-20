"""Инициализация базы данных REPA (создание таблиц для dev / SQLite)."""

import logging
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config import settings
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import get_engine

logger = logging.getLogger(__name__)


def _is_postgres(url: str) -> bool:
    """Проверить, что используется PostgreSQL."""
    return url.startswith("postgresql")


async def _ensure_pg_extensions(sync_conn) -> None:
    """Создать полезные EXTENSION'ы в PostgreSQL (idempotent)."""
    sync_conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    sync_conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS btree_gin;")


async def init_db() -> None:
    """
    Упрощённая инициализация БД.

    ⚙️  Для SQLite просто создаёт таблицы через SQLAlchemy.
    ⚙️  Для PostgreSQL — дополнительно проверяет расширения.
    ⚙️  Миграции Alembic можно запускать вручную: `alembic upgrade head`.
    """
    logger.info("Инициализация базы данных...")

    engine: AsyncEngine = get_engine()

    async with engine.begin() as conn:
        if _is_postgres(settings.db_url):
            await conn.run_sync(_ensure_pg_extensions)
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Таблицы успешно созданы (или уже существовали).")
