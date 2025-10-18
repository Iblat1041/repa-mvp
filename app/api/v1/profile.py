"""Профиль/сводка (1.5)."""

from fastapi import APIRouter, Depends

from app.core.security import require_user
from app.schemas.common import User
from app.schemas.profile import Counters, ProfileSummary
from app.services.store import store

router = APIRouter()


@router.get("/profile/summary", response_model=ProfileSummary)
def profile_summary(user: User = Depends(require_user)) -> ProfileSummary:
    """Вернуть краткую информацию профиля для шапки/кабинета."""
    reqs = store.requests_by_owner(user.id)
    active = sum(1 for r in reqs if r["status"] in {"PENDING", "RUNNING", "ANALYZING"})
    return ProfileSummary(
        user=user,
        counters=Counters(requests_total=len(reqs), active=active),
        balance={"currency": "RUB", "amount": 0},
    )
