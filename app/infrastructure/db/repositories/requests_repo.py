"""Репозиторий заявок (Requests)."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.tables import RequestDB


class RequestsRepo:
    """Операции над заявками."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        request_id: str,
        owner_id: Optional[str],
        query: str,
        language: str,
        sources_csv: str,
        period_start: date,
        period_end: date,
        applied_promo: Optional[str],
    ) -> RequestDB:
        """Создать новую заявку."""
        row = RequestDB(
            id=request_id,
            owner_id=owner_id,
            query=query,
            language=language,
            sources=sources_csv,
            period_start=period_start,
            period_end=period_end,
            status="PENDING",
            progress=0,
            eta_seconds=10,
            applied_promo=applied_promo,
        )
        self.session.add(row)
        await self.session.flush()
        return row

    async def get(self, request_id: str) -> Optional[RequestDB]:
        """Получить заявку по ID."""
        res = await self.session.execute(select(RequestDB).where(RequestDB.id == request_id))
        return res.scalar_one_or_none()

    async def by_owner(self, owner_id: str) -> list[RequestDB]:
        """Получить все заявки владельца."""
        res = await self.session.execute(select(RequestDB).where(RequestDB.owner_id == owner_id))
        return list(res.scalars().all())

    async def update_progress(self, request_id: str, step: int) -> None:
        """Обновить прогресс и ETA (эмуляция фоновой работы)."""
        await self.session.execute(
            update(RequestDB)
            .where(RequestDB.id == request_id)
            .values(progress=step, eta_seconds=max(0, 10 - step // 10))
        )

    async def mark_status(self, request_id: str, status: str) -> None:
        """Изменить статус заявки."""
        await self.session.execute(update(RequestDB).where(RequestDB.id == request_id).values(status=status))

    @staticmethod
    def calc_period(tariff_code: str, start: Optional[date]) -> tuple[date, date]:
        """Посчитать период по тарифу и стартовой дате."""
        days = {"WEEK": 7, "MONTH": 30, "QUARTER": 90}[tariff_code]
        if start is None:
            start = date.today() - timedelta(days=days)
        end = start + timedelta(days=days - 1)
        return start, end
