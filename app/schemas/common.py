"""Общие (переиспользуемые) схемы Pydantic."""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """Мини-модель пользователя, которая прокидывается в JWT."""

    id: str
    email: EmailStr


class Period(BaseModel):
    """Интервал дат, используемый запросами и тарифами."""

    start_date: date
    end_date: date


class Price(BaseModel):
    """Денежное представление (оценка/стоимость)."""

    currency: str = "RUB"
    amount: int = Field(ge=0)
    discount: int = Field(ge=0, le=100, default=0)


class ErrorResponse(BaseModel):
    """Единый формат ошибок API."""

    error: str
    message: str
    details: Optional[dict] = None


RequestStatus = Literal[
    "PENDING",
    "RUNNING",
    "COLLECTED",
    "ANALYZING",
    "READY",
    "NO_DATA",
    "FAILED",
]
