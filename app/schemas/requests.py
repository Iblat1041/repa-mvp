"""Схемы запросов на сбор публикаций и статуса."""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.common import Period, Price, RequestStatus


class ValidateQueryIn(BaseModel):
    """Входные данные для валидации поисковой фразы (1.1)."""

    query: str = Field(min_length=2, max_length=256)
    locale: str = "ru"
    allow_operators: bool = True


class ValidateQueryOut(BaseModel):
    """Результат валидации с нормализацией и предупреждениями."""

    ok: bool
    normalized_query: str
    tokens: list[str]
    estimated_cost: Price
    warnings: list[str] = []


class CreateRequestIn(BaseModel):
    """Входные данные для создания запроса (1.3)."""

    query: str = Field(min_length=2, max_length=256)
    tariff_code: Literal["WEEK", "MONTH", "QUARTER"]
    start_date: Optional[date] = None
    sources: Optional[list[Literal["rss", "web"]]] = None
    language: Optional[Literal["ru", "en"]] = "ru"
    apply_promocode: Optional[str] = None


class CreateRequestOut(BaseModel):
    """Ответ при создании запроса (Accepted)."""

    request_id: str
    status: RequestStatus
    price: Price
    period: Period


class RequestStatusOut(BaseModel):
    """Модель короткого статуса для опроса прогресса."""

    request_id: str
    status: RequestStatus
    progress: int = 0
    eta_seconds: int | None = None
