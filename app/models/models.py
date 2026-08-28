from uuid import uuid4, UUID
from sqlalchemy import ForeignKey, String, func, Numeric, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal
from datetime import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_accounts"

    transfer_relationship: Mapped[list["Transfer"]] = relationship("Transfer", back_populates="user_relationship")
    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_name: Mapped[str] = mapped_column(String(30), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal('0.0'), nullable=False)

    __table_args__ = (
        CheckConstraint("balance >= 0.0", name="check_positive_balance"),
    )

class Transaction(Base):
    __tablename__ = "transactions"

    transfer_relationship: Mapped[list["Transfer"]] = relationship("Transfer", back_populates="transaction_relationship")
    transaction_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    transaction_date: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    transaction_description: Mapped[str] = mapped_column(String(100), nullable=False)

class Transfer(Base):
    __tablename__ = "transfers"

    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.transaction_id"), nullable=False)
    transaction_relationship: Mapped["Transaction"] = relationship("Transaction", back_populates="transfer_relationship")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_accounts.user_id"), nullable=False)
    user_relationship: Mapped["User"] = relationship("User", back_populates="transfer_relationship")
    transfer_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    transfer_type: Mapped[bool] = mapped_column(nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal('0.0'), nullable=False)

    __table_args__ = (
        CheckConstraint("value > 0.0", name="check_positive_value"),
    )