"""Схемы тарифов."""

from typing import List, Literal

from pydantic import BaseModel

TariffCode = Literal["WEEK", "MONTH", "QUARTER"]


class Tariff(BaseModel):
    """Представление тарифа в API."""

    code: TariffCode
    title: str
    days: int
    price: int


class TariffsResponse(BaseModel):
    """Ответ со списком тарифов."""

    items: List[Tariff]
    currency: str = "RUB"
