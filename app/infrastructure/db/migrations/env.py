"""Alembic environment file (async version)."""

from logging.config import fileConfig
import asyncio
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# Импорты твоего проекта
from core.config import settings
from core.db import Base

# Настройка логирования
config = context.config
fileConfig(config.config_file_name)

# Метаданные из ORM
target_metadata = Base.metadata
database_url = settings.db_url


def run_migrations_offline() -> None:
    """Оффлайн-режим: генерирует SQL без подключения к БД."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Онлайн-режим: применяет миграции через async engine."""
    connectable = create_async_engine(database_url, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection) -> None:
    """Основная логика миграции."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
