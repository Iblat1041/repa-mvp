"""Демо-режим (SQLAlchemy)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories.demo_repo import DemoRepo
from app.infrastructure.db.session import get_session

router = APIRouter()


@router.post("/demo/start")
async def start_demo(session: AsyncSession = Depends(get_session)) -> dict:
    """Создать демо-сессию и вернуть её метаданные."""
    row = await DemoRepo(session).create()
    await session.commit()
    meta = await DemoRepo(session).meta(row.id)
    return {"demo_request_id": row.id, "expires_at": meta["expires_at"], "limits": {"max_items": meta["max_items"]}}
