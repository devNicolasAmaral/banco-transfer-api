from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import AccountEntry, Transfer, User


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()

        session.query(AccountEntry).delete()
        session.query(Transfer).delete()
        session.query(User).delete()

        session.commit()
        session.close()
