"""Список публикаций c фильтрами (SQLAlchemy)."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories.publications_repo import PublicationsRepo
from app.infrastructure.db.repositories.requests_repo import RequestsRepo
from app.infrastructure.db.session import get_session
from app.schemas.publications import PublicationsResponse

router = APIRouter()


@router.get("/publications", response_model=PublicationsResponse)
async def list_publications(
    request_id: str = Query(..., description="ID заявки или demo_id"),
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    source: Optional[str] = None,
    sentiment: Optional[str] = None,
    lang: Optional[str] = None,
    offset: int = 0,
    limit: int = 50,
    sort: str = "-published_at",
    session: AsyncSession = Depends(get_session),
) -> PublicationsResponse:
    """Вернуть публикации по фильтрам/пагинации."""
    req = await RequestsRepo(session).get(request_id)
    is_demo = await _is_demo(request_id, session)
    if not req and not is_demo:
        raise HTTPException(status_code=404, detail="request_not_found")

    def _set(val: Optional[str]) -> Optional[set[str]]:
        return set(v.strip() for v in val.split(",")) if val else None

    repo = PublicationsRepo(session)
    page = await repo.list_filtered(
        request_id=request_id,
        date_from=date_from,
        date_to=date_to,
        sources=_set(source),
        sentiments=_set(sentiment),
        langs=_set(lang),
        offset=offset,
        limit=limit,
        sort=sort,
    )
    return PublicationsResponse(
        total=page["total"],
        items=[
            # Pydantic сам преобразует ORM-объекты; можно вернуть напрямую
            p
            for p in page["items"]
        ],
        offset=offset,
        limit=limit,
    )


async def _is_demo(rid: str, session: AsyncSession) -> bool:
    from app.infrastructure.db.repositories.demo_repo import DemoRepo

    return await DemoRepo(session).is_active(rid)
