# app/core/config.py
"""Конфигурация приложения (Pydantic Settings v2 + pydantic-settings)."""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Параметры конфигурации, читаемые из .env и окружения."""

    # --- CORS ---
    cors_allow_origins: List[str] = Field(default=["http://localhost:5173"])

    # --- БД ---
    db_url: str = Field(default="sqlite+aiosqlite:///./repa.sqlite3")
    echo_sql: bool = Field(default=False)
    auto_create_tables: bool = Field(
        default=True,
        description="В dev создаёт таблицы автоматически; в проде использовать Alembic.",
    )

    # --- JWT ---
    jwt_secret: str = Field(default="dev-secret")
    jwt_issuer: str = Field(default="repa")
    jwt_audience: str = Field(default="repa-users")
    jwt_exp_minutes: int = Field(default=60 * 12)

    # --- Бизнес-настройки ---
    currency: str = Field(default="RUB")
    demo_ttl_days: int = Field(default=7)
    promo_default_percent: int = Field(default=10)

    # --- Метаданные приложения ---
    app_name: str = Field(default="REPA-MVP")
    app_version: str = Field(default="0.2.0")

    # Конфигурация модели (v2)
    model_config = SettingsConfigDict(
        env_prefix="REPA_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
