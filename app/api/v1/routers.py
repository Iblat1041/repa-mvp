"""Регистрация всех роутеров v1 для FastAPI."""

from fastapi import APIRouter

from app.api.v1 import (
    analytics,
    auth,
    demo,
    payments,
    profile,
    publications,
    promocodes,
    requests,
    tariffs,
)

router = APIRouter()

# Подключаем все роутеры к единому router
router.include_router(auth.router, prefix="/v1", tags=["auth"])
router.include_router(tariffs.router, prefix="/v1", tags=["tariffs"])
router.include_router(requests.router, prefix="/v1", tags=["requests"])
router.include_router(publications.router, prefix="/v1", tags=["publications"])
router.include_router(analytics.router, prefix="/v1", tags=["analytics"])
router.include_router(profile.router, prefix="/v1", tags=["profile"])
router.include_router(promocodes.router, prefix="/v1", tags=["promocodes"])
router.include_router(payments.router, prefix="/v1", tags=["payments"])
router.include_router(demo.router, prefix="/v1", tags=["demo"])
