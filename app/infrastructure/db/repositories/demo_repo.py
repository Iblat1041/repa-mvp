"""Репозиторий демо-сессий."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.infrastructure.db.tables import DemoDB


class DemoRepo:
    """Создание и валидация демо-сессий."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self) -> DemoDB:
        """Создать демо-сессию с TTL и лимитом на кол-во публикаций."""
        did = self._generate_id()
        row = DemoDB(
            id=did,
            expires_at=datetime.now(tz=timezone.utc) + timedelta(days=settings.demo_ttl_days),
            max_items=20,
        )
        self.session.add(row)
        await self.session.flush()
        return row

    async def is_active(self, demo_id: str) -> bool:
        """Проверить, что демо существует и не истекло."""
        res = await self.session.execute(select(DemoDB).where(DemoDB.id == demo_id))
        row = res.scalar_one_or_none()
        return bool(row and row.expires_at > datetime.now(tz=timezone.utc))

    async def meta(self, demo_id: str) -> dict:
        """Вернуть метаданные демо."""
        row = await self.session.get(DemoDB, demo_id)
        return {"expires_at": row.expires_at, "max_items": row.max_items}

    @staticmethod
    def _generate_id() -> str:
        """Сгенерировать короткий id."""
        import secrets
        return "demo_" + secrets.token_hex(4)
