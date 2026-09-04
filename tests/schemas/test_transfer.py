from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas import TransferCreate


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


def test_transfer_create_rejects_same_account() -> None:
    with pytest.raises(ValidationError):
        TransferCreate(
            sender_id=SENDER_ID,
            receiver_id=SENDER_ID,
            amount=Decimal("100.00"),
            description="Pagamento",
        )

@pytest.mark.parametrize(
    "amount",
    [
        Decimal("0.00"),
        Decimal("-1.00"),
        Decimal("100.123")
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