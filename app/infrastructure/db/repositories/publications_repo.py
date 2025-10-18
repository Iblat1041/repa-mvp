"""Репозиторий публикаций (Publications)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Select, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.tables import PublicationDB


class PublicationsRepo:
    """Операции над публикациями."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def seed_fake(self, request_id: str, count: int = 16) -> None:
        """Сгенерировать фейковые публикации (эмуляция Scrapy)."""
        import random

        items = []
        for i in range(count):
            dt = datetime.utcnow() - func.random() * 10000  # типовой приём не сработает: fallback
            # из-за func.random в python — сделаем без SQL:
            from datetime import timedelta

            dt_py = datetime.utcnow() - timedelta(days=random.randint(0, 20), hours=random.randint(0, 23))
            items.append(
                PublicationDB(
                    request_id=request_id,
                    title=f"Публикация №{i + 1} для {request_id}",
                    url=f"https://news.example/{request_id}/{i}",
                    published_at=dt_py,
                    source=random.choice(["rss", "web"]),
                    lang=random.choice(["ru", "en"]),
                    sentiment=random.choice([None, "neg", "neu", "pos"]),
                    entities=None,
                )
            )
        self.session.add_all(items)
        await self.session.flush()

    async def list_filtered(
        self,
        *,
        request_id: str,
        date_from: Optional[datetime],
        date_to: Optional[datetime],
        sources: Optional[set[str]],
        sentiments: Optional[set[str]],
        langs: Optional[set[str]],
        offset: int,
        limit: int,
        sort: str,
    ) -> dict:
        """Вернуть публикации по фильтрам и пагинации."""
        q: Select = select(PublicationDB).where(PublicationDB.request_id == request_id)

        if date_from:
            q = q.where(PublicationDB.published_at >= date_from)
        if date_to:
            q = q.where(PublicationDB.published_at <= date_to)
        if sources:
            q = q.where(PublicationDB.source.in_(sources))
        if sentiments:
            # None трактуем как 'neu' по умолчанию — см. MVP
            q = q.where(PublicationDB.sentiment.in_(sentiments))
        if langs:
            q = q.where(PublicationDB.lang.in_(langs))

        # сортировка
        dir_desc = sort.startswith("-")
        key = sort.lstrip("-")
        if key == "published_at":
            q = q.order_by(desc(PublicationDB.published_at) if dir_desc else asc(PublicationDB.published_at))

        # total
        total = (await self.session.execute(select(func.count()).select_from(q.subquery()))).scalar_one()

        # page
        rows = (await self.session.execute(q.offset(offset).limit(min(limit, 100)))).scalars().all()
        return {"total": total, "items": rows}
