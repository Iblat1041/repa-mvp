"""Эндпоинт тарифов (1.2)."""

from fastapi import APIRouter

from app.schemas.tariffs import Tariff, TariffsResponse

router = APIRouter()


@router.get("/tariffs", response_model=TariffsResponse)
def list_tariffs() -> TariffsResponse:
    """Вернуть активные тарифы и цены (статично для MVP)."""
    items = [
        Tariff(code="WEEK", title="Неделя", days=7, price=199),
        Tariff(code="MONTH", title="Месяц", days=30, price=499),
        Tariff(code="QUARTER", title="Квартал", days=90, price=1299),
    ]
    return TariffsResponse(items=items, currency="RUB")
