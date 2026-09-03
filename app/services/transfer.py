from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    AccountEntry,
    EntryType,
    Transfer,
    User,
)
from app.schemas import TransferCreate
from app.services.exceptions import (
    InsufficientBalanceError,
    UserNotFoundError,
)


def _get_user_for_update(
    session: Session,
    sender_id: UUID,
    receiver_id: UUID,
) -> tuple[User, User]:
    statement = (
        select(User)
        .where(User.user_id.in_([sender_id, receiver_id]))
        .order_by(User.user_id)
        .with_for_update()
    )

    users = {
        user.user_id: user
        for user in session.scalars(statement)
    }

    if sender_id not in users:
        raise UserNotFoundError(sender_id)

    if receiver_id not in users:
        raise UserNotFoundError(receiver_id)

    return users[sender_id], users[receiver_id]


def create_transfer(
    session: Session,
    data: TransferCreate,
) -> Transfer:
    with session.begin():
        sender, receiver = _get_user_for_update(
            session,
            data.sender_id,
            data.receiver_id,
        )

        if sender.balance < data.amount:
            raise InsufficientBalanceError(
                user_id=sender.user_id,
                balance=sender.balance,
                amount=data.amount,
            )

        sender.balance -= data.amount
        receiver.balance += data.amount

        transfer = Transfer(description=data.description)
        transfer.entries = [
            AccountEntry(
                user=sender,
                entry_type=EntryType.DEBIT,
                amount=data.amount,
            ),
            AccountEntry(
                user=receiver,
                entry_type=EntryType.CREDIT,
                amount=data.amount,
            ),
        ]

        session.add(transfer)
        session.flush()

    return transfer