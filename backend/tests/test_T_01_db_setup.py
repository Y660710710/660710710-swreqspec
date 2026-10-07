from __future__ import annotations

from sqlalchemy import inspect
from sqlalchemy import create_engine

from app.db.migrations import upgrade


def test_database_schema_for_booking_setup():
    engine = create_engine("sqlite:///:memory:", future=True)

    upgrade(engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {"slots", "bookings", "audit_logs"}.issubset(tables)

    booking_columns = {column["name"] for column in inspector.get_columns("bookings")}
    assert "hn" in booking_columns
    assert "national_id" not in booking_columns

    slot_columns = {column["name"] for column in inspector.get_columns("slots")}
    assert {"slot_date", "start_time", "package_code", "capacity", "remaining"}.issubset(slot_columns)

    audit_columns = {column["name"] for column in inspector.get_columns("audit_logs")}
    assert {"actor_id", "action", "hn", "accessed_at"}.issubset(audit_columns)
