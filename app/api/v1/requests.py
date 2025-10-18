"""Запросы: валидация (1.1), создание (1.3), статус (SQLAlchemy)."""

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_current_user
from app.infrastructure.db.repositories.publications_repo import PublicationsRepo
from app.infrastructure.db.repositories.requests_repo import RequestsRepo
from app.infrastructure.db.session import get_session
from app.infrastructure.db.tables import RequestDB
from app.schemas.common import Period, Price, User
from app.schemas.requests import (
    CreateRequestIn,
    CreateRequestOut,
    RequestStatusOut,
    ValidateQueryIn,
    ValidateQueryOut,
)

router = APIRouter()


@router.post("/requests/validate-query", response_model=ValidateQueryOut)
async def validate_query(payload: ValidateQueryIn) -> ValidateQueryOut:
    """Проверить и нормализовать поисковую фразу (1.1)."""
    q = payload.query.strip()
    if len(q) < 2:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="query too short")
    tokens = [t for t in q.replace('"', "").split() if len(t) > 1]
    estimated = Price(currency=settings.currency, amount=0, discount=0)
    return ValidateQueryOut(ok=True, normalized_query=q, tokens=tokens, estimated_cost=estimated, warnings=[])


def _period_from_tariff(tariff_code: str, start: Optional[date]) -> Period:
    days = {"WEEK": 7, "MONTH": 30, "QUARTER": 90}[tariff_code]
    if start is None:
        start = date.today() - timedelta(days=days)
    end = start + timedelta(days=days - 1)
    return Period(start_date=start, end_date=end)


@router.post("/requests", response_model=CreateRequestOut, status_code=status.HTTP_202_ACCEPTED)
async def create_request(
    payload: CreateRequestIn,
    bg: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    user: Optional[User] = Depends(get_current_user),
) -> CreateRequestOut:
    """Создать заявку и запустить фоновую эмуляцию сбора данных (1.3)."""
    if payload.tariff_code not in {"WEEK", "MONTH", "QUARTER"}:
        raise HTTPException(status_code=400, detail="unknown_tariff")

    repo = RequestsRepo(session)
    period = _period_from_tariff(payload.tariff_code, payload.start_date)
    rid = _gen_id("req")

    row = await repo.create(
        request_id=rid,
        owner_id=user.id if user else None,
        query=payload.query,
        language=payload.language or "ru",
        sources_csv=",".join(payload.sources or ["rss", "web"]),
        period_start=period.start_date,
        period_end=period.end_date,
        applied_promo=payload.apply_promocode,
    )
    await session.commit()

    bg.add_task(_background_collect, rid)
    price = Price(currency=settings.currency, amount=_quote(payload.tariff_code), discount=0)
    return CreateRequestOut(request_id=row.id, status=row.status, price=price, period=period)


@router.get("/requests/{request_id}/status", response_model=RequestStatusOut)
async def request_status(
    request_id: str,
    session: AsyncSession = Depends(get_session),
) -> RequestStatusOut:
    """Опросить статус обработки заявки."""
    repo = RequestsRepo(session)
    row = await repo.get(request_id)
    if not row:
        raise HTTPException(status_code=404, detail="request_not_found")
    return RequestStatusOut(
        request_id=row.id,
        status=row.status,
        progress=row.progress,
        eta_seconds=row.eta_seconds,
    )


def _quote(tariff_code: str) -> int:
    return {"WEEK": 199, "MONTH": 499, "QUARTER": 1299}[tariff_code]


def _gen_id(prefix: str) -> str:
    import secrets
    return f"{prefix}_{secrets.token_hex(4)}"


async def _background_collect(request_id: str) -> None:
    """Асинхронная «фоновая» эмуляция парсинга с записью в БД."""
    from asyncio import sleep
    from sqlalchemy.ext.asyncio import AsyncSession

    session_maker = __import__("app.infrastructure.db.session", fromlist=["get_session"]).infrastructure.db.session
    session_factory = session_maker.get_session_factory()

    async with session_factory() as session:  # type: AsyncSession
        req_repo = RequestsRepo(session)
        pubs_repo = PublicationsRepo(session)

        # Прогресс (эмуляция)
        for p in (10, 25, 40, 65, 85):
            await req_repo.update_progress(request_id, p)
            await session.commit()
            await sleep(0.25)

        # После «сбора» — сгенерируем публикации
        await pubs_repo.seed_fake(request_id, count=16)
        await req_repo.update_progress(request_id, 100)
        await req_repo.mark_status(request_id, "READY")
        await session.commit()
