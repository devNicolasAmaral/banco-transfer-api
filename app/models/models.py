from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import uuid4, UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class EntryType(str, Enum):
    CREDIT = "C"
    DEBIT = "D"


class User(Base):
    __tablename__ = "user_accounts"

    entries: Mapped[list["AccountEntry"]] = relationship(
        "AccountEntry",
        back_populates="user",
    )
    user_id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid4,
    )
    user_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        default=Decimal('0.00'),
        server_default="0.00",
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "balance >= 0.00",
            name="check_non_negative_balance",
        ),
    )


class Transfer(Base):
    __tablename__ = "transfers"

    entries: Mapped[list["AccountEntry"]] = relationship(
        "AccountEntry",
        back_populates="transfer",
    )
    transfer_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


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
    transfer: Mapped["Transfer"] = relationship(
        "Transfer",
        back_populates="entries",
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_accounts.user_id"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
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
