from collections.abc import Generator
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.main import app
from app.models import User


def test_create_user_endpoint_returns_created_status(
    db_session: Session,
) -> None:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    try:
        response = client.post(
            "/users",
            json={"user_name": "Nicolas"},
        )

        response_data = response.json()

        get_response = client.get(
            f"/users/{response_data['user_id']}",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201

    assert response_data["user_name"] == "Nicolas"
    assert Decimal(str(response_data["balance"])) == Decimal("0.00")
    assert response_data["user_id"]

    assert get_response.status_code == 200

    get_data = get_response.json()

    assert get_data["user_id"] == response_data["user_id"]
    assert get_data["user_name"] == "Nicolas"
    assert Decimal(str(get_data["balance"])) == Decimal("0.00")

    user = db_session.get(
        User,
        UUID(response_data["user_id"]),
    )

    assert user is not None
    assert user.user_name == "Nicolas"
    assert user.balance == Decimal("0.00")