"""Репозиторий платежей (заглушка провайдера)."""

from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.tables import PaymentDB


class PaymentsRepo:
    """Создание платежа и приём вебхуков статуса."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, *, request_id: str, link: str, provider: str = "stub") -> PaymentDB:
        """Создать запись о платеже для заявки."""
        payment = PaymentDB(request_id=request_id, link=link, provider=provider, status="created")
        self.session.add(payment)
        await self.session.flush()
        return payment

    async def set_status(self, *, request_id: str, status: str) -> bool:
        """Обновить статус платежа."""
        res = await self.session.execute(select(PaymentDB).where(PaymentDB.request_id == request_id))
        row = res.scalar_one_or_none()
        if not row:
            return False
        await self.session.execute(update(PaymentDB).where(PaymentDB.id == row.id).values(status=status))
        return True
