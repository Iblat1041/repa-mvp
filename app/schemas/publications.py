"""Схемы публикаций и выдачи с пагинацией."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Publication(BaseModel):
    """Нормализованная единица публикации (результат парсинга)."""

    id: str
    title: str
    url: str
    published_at: datetime
    source: Literal["rss", "web"]
    lang: Literal["ru", "en"]
    sentiment: Literal["neg", "neu", "pos"] | None = None
    request_id: str
    entities: list[str] = []


class PublicationsResponse(BaseModel):
    """Пагинированный список публикаций."""

    total: int
    items: list[Publication]
    offset: int = 0
    limit: int = 50
