"""Репозиторий промокодов."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.utctime import utcnow  # ✅ единый безопасный UTC-хелпер
from app.infrastructure.db.tables import PromoCodeDB


class PromosRepo:
    """Операции с промокодами: выдача, проверка, погашение."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _as_utc_aware(dt: Optional[datetime]) -> Optional[datetime]:
        """
        Преобразовать naive datetime из SQLite в UTC-aware.

        SQLite не хранит информацию о временной зоне, поэтому datetime,
        извлечённые через SQLAlchemy, могут быть без tzinfo.
        """
        if dt is None:
            return None
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt

    async def issue(self, *, email: str, reason: str) -> PromoCodeDB:
        """Выдать промокод (один на email)."""
        exists = await self.session.execute(
            select(PromoCodeDB).where(PromoCodeDB.issued_to_email == email)
        )
        if exists.scalar_one_or_none():
            raise ValueError("already_issued")

        code = self._generate_code()
        promo = PromoCodeDB(
            code=code,
            discount_percent=settings.promo_default_percent,
            expires_at=utcnow() + timedelta(days=30),  # ✅ всегда aware datetime
            reason=reason,
            redeemed=False,
            issued_to_email=email,
        )
        self.session.add(promo)
        await self.session.flush()
        return promo

    async def validate(self, code: str) -> dict:
        """Проверить валидность кода (существует, не просрочен, не погашен)."""
        row = await self.session.get(PromoCodeDB, code)
        if not row:
            return {"valid": False, "code": code}

        now = utcnow()
        exp = self._as_utc_aware(row.expires_at)

        valid = (not row.redeemed) and (exp > now)

        base = {
            "code": row.code,
            "discount_percent": row.discount_percent,
            "reason": row.reason,
            "expires_at": row.expires_at,
        }
        return {"valid": valid, **base} if valid else {"valid": False, **base}

    async def redeem(self, code: str) -> bool:
        """Пометить код как погашенный."""
        row = await self.session.get(PromoCodeDB, code)
        now = utcnow()
        exp = self._as_utc_aware(row.expires_at) if row else None

        if not row or row.redeemed or exp <= now:
            return False

        await self.session.execute(
            update(PromoCodeDB)
            .where(PromoCodeDB.code == code)
            .values(redeemed=True)
        )
        return True

    @staticmethod
    def _generate_code() -> str:
        """Сгенерировать человекочитаемый код."""
        import secrets

        return "START_" + secrets.token_hex(4).upper()
