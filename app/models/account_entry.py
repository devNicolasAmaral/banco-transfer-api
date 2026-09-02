from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Enum as SqlEnum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import EntryType


if TYPE_CHECKING:
    from app.models.transfer import Transfer
    from app.models.user import User


class AccountEntry(Base):
    __tablename__ = "account_entries"

    entry_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    transfer_id: Mapped[UUID] = mapped_column(
        ForeignKey("transfers.transfer_id"),
        nullable=False,
    )
    transfer: Mapped[Transfer] = relationship(
        "Transfer",
        back_populates="entries",
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_accounts.user_id"),
        nullable=False,
    )
    user: Mapped[User] = relationship(
        "User",
        back_populates="entries",
    )
    entry_type: Mapped[EntryType] = mapped_column(
        SqlEnum(
            EntryType,
            name="entry_type_enum",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("amount > 0.00", name="check_positive_amount"),
    )
