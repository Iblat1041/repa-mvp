# app/core/utctime.py
from datetime import datetime, timezone

def utcnow() -> datetime:
    """Текущее время в UTC с tzinfo."""
    return datetime.now(timezone.utc)
