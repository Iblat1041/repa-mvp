"""Схемы промокодов."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class PromoIssueIn(BaseModel):
    """Выдать промокод по email (плашка онбординга)."""

    email: EmailStr
    reason: str


class PromoIssueOut(BaseModel):
    """Ответ о выдаче промокода."""

    code: str
    discount_percent: int
    expires_at: datetime


class PromoValidateOut(BaseModel):
    """Проверка существующего промокода."""

    valid: bool
    code: str
    discount_percent: int | None = None
    reason: str | None = None
    expires_at: datetime | None = None
