"""Инициализация базы данных REPA (создание таблиц или миграции)."""

import logging
from sqlalchemy import text
from app.core.config import settings
from app.infrastructure.db.base import Base, run_alembic_upgrade
from app.infrastructure.db.session import get_engine

logger = logging.getLogger(__name__)


def _is_postgres(url: str) -> bool:
    """Проверить, что используется PostgreSQL."""
    return url.startswith("postgresql")


def _ensure_pg_extensions(sync_conn) -> None:
    """Создать полезные EXTENSION'ы в PostgreSQL (idempotent)."""
    sync_conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    sync_conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS btree_gin;")


async def init_db(run_migrations: bool | None = None) -> None:
    """Инициализация БД.

    Логика:
      1. Пытаемся выполнить Alembic миграции (`alembic upgrade head`).
      2. Если Alembic не настроен — fallback на create_all() (для dev).
      3. Для PostgreSQL — создаём расширения.
    """
    if run_migrations is None:
        run_migrations = settings.auto_create_tables is False

    engine = get_engine()

    if run_migrations:
        logger.info("Инициализация БД: пытаемся выполнить alembic upgrade head...")
        try:
            ran = await run_alembic_upgrade(engine)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Alembic не сработал: %s", exc)
            ran = False

        if ran:
            logger.info("Alembic миграции применены.")
            return
        else:
            logger.warning("Alembic недоступен — выполняем create_all().")

    # Fallback для dev — просто создать таблицы
    logger.info("Создаём таблицы через metadata.create_all()...")
    async with engine.begin() as conn:
        if _is_postgres(settings.db_url):
            await conn.run_sync(_ensure_pg_extensions)
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Инициализация БД завершена.")
