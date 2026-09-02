from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


if TYPE_CHECKING:
    from app.models.account_entry import AccountEntry


class Transfer(Base):
    __tablename__ = "transfers"

    entries: Mapped[list[AccountEntry]] = relationship(
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
