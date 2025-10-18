"""Авторизация (1.4). Упрощённый вход по email+код."""

from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token
from app.schemas.auth import LoginIn, TokensOut
from app.schemas.common import User

router = APIRouter()

# Псевдо-хранилище кодов (email -> code) для демонстрации.
_FAKE_CODES: dict[str, str] = {}


@router.post("/auth/login", response_model=TokensOut)
def login(payload: LoginIn) -> TokensOut:
    """Войти по email и коду.

    Для упрощения считаем корректным любой код "000000" либо совпадающий
    с сохранённым в памяти (эмуляция рассылки кода по почте).
    """
    code_ok = payload.code == "000000" or _FAKE_CODES.get(payload.email) == payload.code
    if not code_ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_code")

    user = User(id=f"u_{hash(payload.email) & 0xFFFF:X}", email=payload.email)
    token = create_access_token(user)
    return TokensOut(access_token=token, user=user)
