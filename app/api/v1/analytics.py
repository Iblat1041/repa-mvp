"""Агрегаты (упрощённо, считаем в БД выборкой)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories.requests_repo import RequestsRepo
from app.infrastructure.db.session import get_session
from app.infrastructure.db.tables import PublicationDB

router = APIRouter()


@router.get("/analytics/summary")
async def analytics_summary(
    request_id: str = Query(...),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Вернуть компактные агрегаты по публикациям."""
    req = await RequestsRepo(session).get(request_id)
    if not req:
        # допускаем демо
        from app.infrastructure.db.repositories.demo_repo import DemoRepo

        if not await DemoRepo(session).is_active(request_id):
            raise HTTPException(status_code=404, detail="request_not_found")

    # Подсчёты
    total = (
        await session.execute(
            select(func.count()).select_from(PublicationDB).where(PublicationDB.request_id == request_id)
        )
    ).scalar_one()

    def count_by(col, value):
        return (
            session.execute(
                select(func.count())
                .select_from(PublicationDB)
                .where(PublicationDB.request_id == request_id)
                .where(col == value)
            )
        )

    rss = (await count_by(PublicationDB.source, "rss")).scalar_one()
    web = (await count_by(PublicationDB.source, "web")).scalar_one()

    neg = (await count_by(PublicationDB.sentiment, "neg")).scalar_one()
    neu = (await count_by(PublicationDB.sentiment, "neu")).scalar_one()
    pos = (await count_by(PublicationDB.sentiment, "pos")).scalar_one()

    return {"count": total, "sources": {"rss": rss, "web": web}, "sentiments": {"neg": neg, "neu": neu, "pos": pos}}
