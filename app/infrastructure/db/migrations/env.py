"""Alembic environment file (асинхронная версия для REPA)."""

import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# Импорты проекта
from app.core.config import settings
from app.infrastructure.db.base import Base

# -------------------------------------------------------------------------
# Конфигурация Alembic
# -------------------------------------------------------------------------

# Объект конфигурации, доступный из alembic.ini
config = context.config

# Подключаем логирование, если в ini-файле оно включено
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей (используются для автогенерации миграций)
target_metadata = Base.metadata

# URL базы данных из pydantic Settings (.env)
config.set_main_option("sqlalchemy.url", settings.db_url)
database_url = settings.db_url


# -------------------------------------------------------------------------
# Оффлайн-режим (генерация SQL без подключения к БД)
# -------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Запускает миграции в оффлайн-режиме."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------------------------------
# Онлайн-режим (реальное применение миграций к БД)
# -------------------------------------------------------------------------
def do_run_migrations(connection) -> None:
    """Основная логика миграции."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Асинхронное выполнение миграций через SQLAlchemy async engine."""
    connectable: AsyncEngine = create_async_engine(database_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# -------------------------------------------------------------------------
# Точка входа
# -------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
