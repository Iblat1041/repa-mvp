"""Точка входа FastAPI-приложения REPA MVP."""

from fastapi import FastAPI
from app.api.v1 import analytics, publications, recommendations, requests
from app.core.config import Settings


def get_settings() -> Settings:
    """Загружает конфигурацию из .env."""
    return Settings()


app = FastAPI(
    title="REPA Backend",
    version="0.1.0",
    description="MVP сервиса для анализа публикаций и рекомендаций по PR",
)


@app.get("/health")
async def health_check() -> dict:
    """Проверка состояния приложения."""
    return {"status": "ok", "message": "REPA API is running"}


# Подключение маршрутов
app.include_router(requests.router, prefix="/api/v1", tags=["Requests"])
app.include_router(publications.router, prefix="/api/v1", tags=["Publications"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["Recommendations"])
