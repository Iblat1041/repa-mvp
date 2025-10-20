"""Профиль/сводка (1.5). Читаем счётчики из БД."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_user
from app.infrastructure.db.repositories.requests_repo import RequestsRepo
from app.infrastructure.db.session import get_session
from app.schemas.common import User
from app.schemas.profile import Counters, ProfileSummary

router = APIRouter()


@router.get("/profile/summary", response_model=ProfileSummary)
async def profile_summary(
    user: User = Depends(require_user),
    session: AsyncSession = Depends(get_session),
) -> ProfileSummary:
    """Вернуть краткую информацию профиля для шапки/кабинета на основе БД."""
    repo = RequestsRepo(session)
    reqs = await repo.by_owner(user.id)

    active_statuses = {"PENDING", "RUNNING", "ANALYZING"}
    active = sum(1 for r in reqs if r.status in active_statuses)

    return ProfileSummary(
        user=user,
        counters=Counters(requests_total=len(reqs), active=active),
        balance={"currency": "RUB", "amount": 0},
    )
