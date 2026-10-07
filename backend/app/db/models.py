from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Slot(Base):
    __tablename__ = "slots"

    # Supports FR-BKG-01, FR-BKG-06, CON-TECH-01
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slot_date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    start_time: Mapped[str] = mapped_column(String(5), nullable=False)
    package_code: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
    capacity: Mapped[int] = mapped_column(nullable=False)
    remaining: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    # Supports FR-BKG-02, FR-BKG-04, IF-HIS-01
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), nullable=False, index=True)
    booking_date: Mapped[str] = mapped_column(String(10), nullable=False)
    queue_no: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="confirmed")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    # Supports DOM-PDPA-01
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    actor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    accessed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
