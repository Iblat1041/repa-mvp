"""Мини-утилиты JWT и зависимости авторизации."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.schemas.common import User

bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(user: User) -> str:
    """Создать подписанный JWT-токен для пользователя.

    :param user: Модель пользователя с id и email.
    :return: Строка с JWT.
    """
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": user.id,
        "email": user.email,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_exp_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Optional[User]:
    """Получить текущего пользователя по токену или None (гость).

    :param credentials: Заголовок Authorization: Bearer <token>.
    :return: Модель пользователя или None.
    :raises HTTPException: 401 при невалидном токене.
    """
    if not credentials:
        return None

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            key=settings.jwt_secret,
            algorithms=["HS256"],
            audience=settings.jwt_audience,
            options={"require": ["sub", "exp"]},
        )
        return User(id=str(payload["sub"]), email=str(payload.get("email", "")))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid_token: {exc}",
        ) from exc


def require_user(user: Optional[User] = Depends(get_current_user)) -> User:
    """Обязательное наличие авторизованного пользователя.

    :param user: Пользователь (может быть None).
    :return: Пользователь.
    :raises HTTPException: 401 если пользователь не авторизован.
    """
    if not user:
        raise HTTPException(status_code=401, detail="unauthorized")
    return user
