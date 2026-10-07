from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base
from app.db.session import SessionLocal


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine, future=True)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def session_factory():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal.configure(bind=engine)
    yield SessionLocal
    SessionLocal.configure(bind=None)
    engine.dispose()
