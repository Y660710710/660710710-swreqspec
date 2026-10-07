from __future__ import annotations

from sqlalchemy import text


# Supports CON-TECH-01, DOM-PDPA-01, IF-HIS-01
def upgrade(engine):
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                package_code TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                remaining INTEGER NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_slots_slot_date ON slots(slot_date)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_slots_package_code ON slots(package_code)
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hn TEXT NOT NULL,
                slot_id INTEGER NOT NULL,
                booking_date TEXT NOT NULL,
                queue_no TEXT,
                status TEXT NOT NULL DEFAULT 'confirmed',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (slot_id) REFERENCES slots(id)
            )
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_bookings_hn ON bookings(hn)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_bookings_slot_id ON bookings(slot_id)
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_id TEXT NOT NULL,
                action TEXT NOT NULL,
                hn TEXT NOT NULL,
                accessed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_audit_hn ON audit_logs(hn)
        """))
