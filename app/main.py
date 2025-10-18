"""Точка входа FastAPI для проекта REPA (MVP)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import router as v1_router
from app.core.config import settings
from app.infrastructure.db.init_db import init_db


def create_app() -> FastAPI:
    """Фабрика FastAPI-приложения."""
    app = FastAPI(
        title=getattr(settings, "app_name", "REPA"),
        version=getattr(settings, "app_version", "0.2.0"),
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем единый router для всех endpoints v1
    app.include_router(v1_router)

    @app.get("/health", tags=["meta"])
    async def health() -> dict[str, str]:
        """Проверка состояния приложения."""
        return {"status": "ok"}

    @app.on_event("startup")
    async def on_startup() -> None:
        """Создание таблиц или применение миграций при старте."""
        await init_db()

    return app


app = create_app()
