"""Базовый класс ORM-моделей для проекта REPA.
"""

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr


class PreBase:
    """Миксин: задаёт имя таблицы и первичный ключ."""

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        """Имя таблицы совпадает с именем класса в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)


# Все модели наследуются от этого Base
Base = declarative_base(cls=PreBase)
