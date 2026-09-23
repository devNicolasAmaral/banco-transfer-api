from decimal import Decimal

import pytest

from sqlalchemy.orm import Session

from app.models import (
    AccountEntry,
    EntryType,
    Transfer,
    User,
)
from app.schemas import TransferCreate
from app.services import InsufficientBalanceError, create_transfer

def test_create_transfer_updates_balances_and_creates_entries(
    db_session: Session,
) -> None:
    sender = User(
        user_name="Remetente",
        balance=Decimal("100.00"),
    )
    receiver = User(
        user_name="Destinatario",
        balance=Decimal("50.00"),
    )

    db_session.add_all([sender, receiver])
    db_session.flush()

    sender_id = sender.user_id
    receiver_id = receiver.user_id

    db_session.commit()

    transfer_data = TransferCreate(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=Decimal("30.00"),
        description="Pagamento",
    )

    transfer = create_transfer(db_session, transfer_data)

    assert transfer.description == "Pagamento"

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == Decimal("70.00")
    assert receiver.balance == Decimal("80.00")
    assert len(transfer.entries) == 2

    entries_by_type = {
        entry.entry_type: entry
        for entry in transfer.entries
    }

    debit_entry = entries_by_type[EntryType.DEBIT]
    credit_entry = entries_by_type[EntryType.CREDIT]

    assert debit_entry.user_id == sender_id
    assert debit_entry.amount == Decimal("30.00")
    assert credit_entry.user_id == receiver_id
    assert credit_entry.amount == Decimal("30.00")


def test_create_transfer_rejects_insufficient_balance(
        db_session: Session,
) -> None:
    sender = User(
        user_name="Remetente",
        balance=Decimal("20.00"),
    )
    receiver = User(
        user_name="Destinatario",
        balance=Decimal("50.00"),
    )

    db_session.add_all([sender, receiver])
    db_session.flush()

    sender_id = sender.user_id
    receiver_id = receiver.user_id

    assert sender.balance == Decimal("20.00")
    assert receiver.balance == Decimal("50.00")
    
    db_session.commit()

    transfer_data = TransferCreate(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=Decimal("30.00"),
        description="Pagamento",
    )

    with pytest.raises(InsufficientBalanceError):
        create_transfer(db_session, transfer_data)

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == Decimal("20.00")
    assert receiver.balance == Decimal("50.00")
    assert db_session.query(Transfer).count() == 0
    assert db_session.query(AccountEntry).count() == 0
    