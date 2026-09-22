from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas import (
    AccountEntryResponse,
    TransferCreate,
    TransferResponse,
)


SENDER_ID = UUID("00000000-0000-0000-0000-000000000001")
RECEIVER_ID = UUID("00000000-0000-0000-0000-000000000002")


def test_transfer_create_normalizes_valid_data() -> None:
    transfer = TransferCreate.model_validate(
        {
            "sender_id": SENDER_ID,
            "receiver_id": RECEIVER_ID,
            "amount": "100.50",
            "description": "  Pagamento  ",
        }
    )

    assert transfer.amount == Decimal("100.50")
    assert transfer.description == "Pagamento"


def test_transfer_create_rejects_description_with_only_whitespace() -> None:
    with pytest.raises(ValidationError):
        TransferCreate(
            sender_id=SENDER_ID,
            receiver_id=RECEIVER_ID,
            amount=Decimal("100.00"),
            description="   ",
        )


def test_transfer_create_rejects_same_account() -> None:
    with pytest.raises(ValidationError):
        TransferCreate(
            sender_id=SENDER_ID,
            receiver_id=SENDER_ID,
            amount=Decimal("100.00"),
            description="Pagamento",
        )


def test_transfer_create_accepts_minimum_amount() -> None:
    transfer = TransferCreate(
        sender_id=SENDER_ID,
        receiver_id=RECEIVER_ID,
        amount=Decimal("0.01"),
        description="Pagamento",
    )

    assert transfer.amount == Decimal("0.01")


def test_transfer_create_accepts_maximum_amount() -> None:
    transfer = TransferCreate(
        sender_id=SENDER_ID,
        receiver_id=RECEIVER_ID,
        amount=Decimal("99999999.99"),
        description="Pagamento",
    )

    assert transfer.amount == Decimal("99999999.99")


@pytest.mark.parametrize(
    "amount",
    [
        Decimal("0.00"),
        Decimal("-1.00"),
        Decimal("100.123"),
        Decimal("100000000.00"),
    ],
)
def test_transfer_create_rejects_invalid_amount(amount: Decimal) -> None:
    with pytest.raises(ValidationError):
        TransferCreate(
            sender_id=SENDER_ID,
            receiver_id=RECEIVER_ID,
            amount=amount,
            description="Pagamento",
        )


def test_transfer_create_accepts_maximum_description_length() -> None:
    transfer = TransferCreate(
        sender_id=SENDER_ID,
        receiver_id=RECEIVER_ID,
        amount=Decimal("100.00"),
        description="a" * 100,
    )

    assert transfer.description == "a" * 100


@pytest.mark.parametrize(
    "description",
    [
        "",
        "a" * 101,
    ],
)
def test_transfer_create_rejects_invalid_description_length(
    description: str,
) -> None:
    with pytest.raises(ValidationError):
        TransferCreate(
            sender_id=SENDER_ID,
            receiver_id=RECEIVER_ID,
            amount=Decimal("100.00"),
            description=description,
        )


def test_transfer_response_builds_from_transfer_attributes() -> None:
    transfer = type(
        "TransferStub",
        (),
        {
            "transfer_id": "00000000-0000-0000-0000-000000000010",
            "created_at": datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
            "description": "Pagamento",
            "entries": [
                {
                    "entry_id": "00000000-0000-0000-0000-000000000011",
                    "user_id": "00000000-0000-0000-0000-000000000001",
                    "entry_type": "C",
                    "amount": "100.00",
                }
            ],
        },
    )()

    response = TransferResponse.model_validate(transfer)

    assert response.transfer_id == UUID("00000000-0000-0000-0000-000000000010")
    assert response.description == "Pagamento"
    assert len(response.entries) == 1
    assert response.created_at == datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    assert isinstance(response.entries[0], AccountEntryResponse)
