"""Конфигурация приложения (Pydantic Settings)."""

from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Параметры конфигурации, читаемые из окружения."""

    cors_allow_origins: List[str] = Field(default=["*"])

    # БД: SQLite локально, Postgres в проде.
    db_url: str = Field(default="sqlite+aiosqlite:///./repa.sqlite3")
    echo_sql: bool = Field(default=False)
    pool_size: int = Field(default=5)
    auto_create_tables: bool = Field(
        default=True,
        description="В dev создаёт таблицы автоматически; в проде использовать Alembic.",
    )

    # JWT (упрощённо)
    jwt_secret: str = Field(default="dev-secret")
    jwt_issuer: str = Field(default="repa")
    jwt_audience: str = Field(default="repa-users")
    jwt_exp_minutes: int = Field(default=60 * 12)

    # Бизнес-настройки
    currency: str = Field(default="RUB")
    demo_ttl_days: int = Field(default=7)
    promo_default_percent: int = Field(default=10)

    class Config:
        env_prefix = "REPA_"
        case_sensitive = False


settings = Settings()
