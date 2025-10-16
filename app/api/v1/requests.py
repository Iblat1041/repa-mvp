"""Маршруты для работы с запросами на парсинг публикаций."""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List


router = APIRouter()


class RequestCreate(BaseModel):
    """Модель входных данных для создания запроса."""
    query: str
    start_date: datetime
    end_date: datetime


class RequestResponse(BaseModel):
    """Модель ответа API при создании запроса."""
    id: int
    query: str
    status: str
    created_at: datetime


# Мок-данные (вместо БД)
_fake_requests: List[RequestResponse] = []


@router.post("/requests", response_model=RequestResponse)
async def create_request(payload: RequestCreate) -> RequestResponse:
    """Создание нового запроса на парсинг."""
    new_request = RequestResponse(
        id=len(_fake_requests) + 1,
        query=payload.query,
        status="processing",
        created_at=datetime.utcnow(),
    )
    _fake_requests.append(new_request)
    return new_request


@router.get("/requests", response_model=List[RequestResponse])
async def list_requests() -> List[RequestResponse]:
    """Возвращает список всех запросов."""
    return _fake_requests
