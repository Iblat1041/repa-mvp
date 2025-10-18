"""Платежи (эмуляция провайдера, SQLAlchemy)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories.payments_repo import PaymentsRepo
from app.infrastructure.db.repositories.requests_repo import RequestsRepo
from app.infrastructure.db.session import get_session

router = APIRouter()


@router.post("/payments/checkout")
async def checkout(request_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    """Создать платёж и вернуть ссылку на оплату (эмуляция)."""
    if not await RequestsRepo(session).get(request_id):
        raise HTTPException(status_code=404, detail="request_not_found")
    link = f"https://pay.example/checkout?rid={request_id}"
    payment = await PaymentsRepo(session).create(request_id=request_id, link=link)
    await session.commit()
    return {"checkout_url": payment.link}


@router.post("/payments/webhook")
async def webhook(provider: str, request_id: str, status: str, session: AsyncSession = Depends(get_session)) -> dict:
    """Вебхук провайдера: обновляет статус платежа."""
    ok = await PaymentsRepo(session).set_status(request_id=request_id, status=status)
    if not ok:
        raise HTTPException(status_code=404, detail="request_not_found")
    await session.commit()
    return {"ok": True}
