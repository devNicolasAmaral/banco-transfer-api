from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models import EntryType
from app.schemas import AccountEntryResponse


@pytest.mark.parametrize(
    "entry_type",
    [
        EntryType.CREDIT,
        EntryType.DEBIT,
    ],
)
def test_account_entry_response_accepts_valid_entry_type(
    entry_type: EntryType,
) -> None:
    entry = AccountEntryResponse(
        entry_id=UUID("00000000-0000-0000-0000-000000000003"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        entry_type=entry_type,
        amount=Decimal("100.00"),
    )

    assert entry.entry_type == entry_type
    assert entry.amount == Decimal("100.00")


def test_account_entry_response_rejects_invalid_entry_type() -> None:
    with pytest.raises(ValidationError):
        AccountEntryResponse(
            entry_id=UUID("00000000-0000-0000-0000-000000000003"),
            user_id=UUID("00000000-0000-0000-0000-000000000001"),
            entry_type="INVALID",  # pyright: ignore[reportArgumentType]
            amount=Decimal("100.00"),
        )


def test_account_entry_response_builds_from_attributes() -> None:
    entry = type(
        "EntryStub",
        (),
        {
            "entry_id": "00000000-0000-0000-0000-000000000021",
            "user_id": "00000000-0000-0000-0000-000000000001",
            "entry_type": "C",
            "amount": "100.00",
        },
    )()

    response = AccountEntryResponse.model_validate(entry)

    assert response.entry_id == UUID("00000000-0000-0000-0000-000000000021")
    assert response.user_id == UUID("00000000-0000-0000-0000-000000000001")
    assert response.entry_type == EntryType.CREDIT
    assert response.amount == Decimal("100.00")
