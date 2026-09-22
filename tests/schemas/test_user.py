from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, UserResponse


def test_user_create_removes_surrounding_whitespace() -> None:
    user = UserCreate(user_name="   Nicolas   ")

    assert user.user_name == "Nicolas"


def test_user_create_rejects_name_with_only_whitespace() -> None:
    with pytest.raises(ValidationError):
        UserCreate(user_name="   ")


@pytest.mark.parametrize(
    "user_name",
    [
        "abc",
        "a" * 30,
    ],
)
def test_user_create_accepts_boundary_name_lengths(user_name: str) -> None:
    user = UserCreate(user_name=user_name)

    assert user.user_name == user_name


@pytest.mark.parametrize(
    "user_name",
    [
        "ab",
        "a" * 31,
    ],
)
def test_user_create_rejects_invalid_name_length(user_name: str) -> None:
    with pytest.raises(ValidationError):
        UserCreate(user_name=user_name)


def test_user_response_builds_from_attributes() -> None:
    user = type(
        "UserStub",
        (),
        {
            "user_id": "00000000-0000-0000-0000-000000000001",
            "user_name": "Nicolas",
            "balance": "100.50",
        },
    )()

    response = UserResponse.model_validate(user)

    assert response.user_id == UUID("00000000-0000-0000-0000-000000000001")
    assert response.user_name == "Nicolas"
    assert response.balance == Decimal("100.50")
