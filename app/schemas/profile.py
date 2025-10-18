"""Схемы для профиля/сводки."""

from pydantic import BaseModel

from app.schemas.common import User


class Counters(BaseModel):
    """Базовые счётчики на главной профиля."""

    requests_total: int
    active: int


class ProfileSummary(BaseModel):
    """Компактные данные профиля."""

    user: User
    counters: Counters
    balance: dict
