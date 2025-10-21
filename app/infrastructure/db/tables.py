from datetime import datetime, date
from app.core.utctime import utcnow
from sqlalchemy import (
    String, Integer, Text, DateTime, Date, Boolean, JSON,
    ForeignKey, UniqueConstraint, Index, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.base import Base

# ---- Users ----
class UserDB(Base):
    __tablename__ = "users"
    # Переопределяем PK на строковый
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

# ---- Requests ----
class RequestDB(Base):
    __tablename__ = "requests"
    # Переопределяем PK на строковый
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    owner_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("users.id"), nullable=True)
    query: Mapped[str] = mapped_column(String(256), index=True)
    language: Mapped[str | None] = mapped_column(String(8), default="ru")
    sources: Mapped[str | None] = mapped_column(String(64), default="rss,web")
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(16), index=True, default="PENDING")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    eta_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    applied_promo: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    __table_args__ = (
        CheckConstraint("progress >= 0 AND progress <= 100", name="chk_progress_bounds"),
        Index("ix_requests_period", "period_start", "period_end"),
    )

# ---- Publications ----
class PublicationDB(Base):
    __tablename__ = "publications"
    # Можно оставить дефолтный INTEGER PK из PreBase (id) ИЛИ явно переопределить:
    # id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(32), ForeignKey("requests.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(16))
    lang: Mapped[str] = mapped_column(String(8), default="ru")
    sentiment: Mapped[str | None] = mapped_column(String(8), nullable=True)
    entities: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    __table_args__ = (
        Index("ix_publications_source_lang", "source", "lang"),
        Index("ix_publications_published", "published_at"),
    )

# ---- Promocodes ----
class PromoCodeDB(Base):
    __tablename__ = "promocodes"
    # У этой модели PK не id, а code → отключаем унаследованный id:
    id = None  # важный трюк, чтобы не было композитного PK
    code: Mapped[str] = mapped_column(String(64), primary_key=True)
    discount_percent: Mapped[int] = mapped_column(Integer, default=10)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str] = mapped_column(String(64))
    redeemed: Mapped[bool] = mapped_column(Boolean, default=False)
    issued_to_email: Mapped[str | None] = mapped_column(String(320), nullable=True, index=True)
    __table_args__ = (CheckConstraint("discount_percent BETWEEN 0 AND 100", name="chk_discount_bounds"),)

# ---- Payments ----
class PaymentDB(Base):
    __tablename__ = "payments"
    request_id: Mapped[str] = mapped_column(String(32), ForeignKey("requests.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(32), default="stub")
    link: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    __table_args__ = (UniqueConstraint("request_id", name="uq_payment_request"),)

# ---- Demos ----
class DemoDB(Base):
    __tablename__ = "demos"
    # PK — строковый demo_id → переопределяем
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    max_items: Mapped[int] = mapped_column(Integer, default=20)
