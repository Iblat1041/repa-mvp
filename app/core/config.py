"""Конфигурация приложения REPA MVP (через Pydantic Settings)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "REPA"
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    secret_key: str = "your-secret-key"

    class Config:
        env_file = ".env"
