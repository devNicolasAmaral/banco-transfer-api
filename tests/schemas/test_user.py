import pytest
from pydantic import ValidationError

from app.schemas import UserCreate


def test_user_create_removes_surrounding_whitespace() -> None:
    user = UserCreate(user_name="   Nicolas   ")

    assert user.user_name == "Nicolas"


def test_user_create_rejects_name_with_only_whitespace() -> None:
    with pytest.raises(ValidationError):
        UserCreate(user_name="   ")