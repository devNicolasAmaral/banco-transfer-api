from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base


if TYPE_CHECKING:
    from app.models.account_entry import AccountEntry


class User(Base):
    __tablename__ = "user_accounts"

    entries: Mapped[list[AccountEntry]] = relationship(
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
