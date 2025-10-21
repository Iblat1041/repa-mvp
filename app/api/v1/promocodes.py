"""Промокоды: выдача, проверка, погашение (SQLAlchemy)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories.promos_repo import PromosRepo
from app.infrastructure.db.session import get_session
from app.schemas.promos import PromoIssueIn, PromoIssueOut, PromoValidateOut

router = APIRouter()


@router.post("/promocodes/request", response_model=PromoIssueOut, status_code=status.HTTP_201_CREATED)
async def issue_promo(payload: PromoIssueIn, session: AsyncSession = Depends(get_session)) -> PromoIssueOut:
    """Выдать одноразовый промокод."""
    repo = PromosRepo(session)
    try:
        promo = await repo.issue(email=payload.email, reason=payload.reason)
        await session.commit()
        return PromoIssueOut(code=promo.code, discount_percent=promo.discount_percent, expires_at=promo.expires_at)
    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/promocodes/validate", response_model=PromoValidateOut)
async def validate_promo(
    code: str = Query(...),
    session: AsyncSession = Depends(get_session)) -> PromoValidateOut:
    """Проверить валидность промокода."""
    info = await PromosRepo(session).validate(code)
    return PromoValidateOut(**info)


@router.post("/promocodes/redeem")
async def redeem_promo(
    code: str = Query(...),
    request_id: str = Query(...),
    session: AsyncSession = Depends(get_session,
    )
) -> dict:
    """Погасить промокод (привязка к заявке делается на уровне RequestDB.applied_promo по твоей бизнес-логике)."""
    ok = await PromosRepo(session).redeem(code)
    if not ok:
        raise HTTPException(status_code=404, detail="unknown_or_expired_code")
    await session.commit()
    return {"ok": True}
