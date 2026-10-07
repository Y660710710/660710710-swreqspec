from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import Base


# Supports CON-TECH-01, IF-HIS-01
def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///:memory:")


# Supports CON-TECH-01
def create_db_engine(database_url: str | None = None):
    url = database_url or get_database_url()
    engine_kwargs = {"future": True}
    if url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **engine_kwargs)


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


# Supports CON-TECH-01, IF-HIS-01
def get_session() -> Session:
    return SessionLocal()


# Supports CON-TECH-01
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
