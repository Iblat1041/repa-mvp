"""Схемы авторизации и токенов."""

from pydantic import BaseModel, EmailStr

from app.schemas.common import User


class LoginIn(BaseModel):
    """Вход по email + код (упрощённо для MVP)."""

    email: EmailStr
    code: str


class TokensOut(BaseModel):
    """Пара токенов/данные пользователя (MVP — только access)."""

    access_token: str
    token_type: str = "bearer"
    user: User
