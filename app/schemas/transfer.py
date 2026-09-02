from __future__ import annotations

from decimal import Decimal
from uuid import UUID
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

from app.schemas.account_entry import AccountEntryResponse


class TransferCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    amount: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )
    description: str = Field(
        min_length=1,
        max_length=100,
    )

    model_config = ConfigDict(str_strip_whitespace=True)

    @model_validator(mode="after")
    def validate_different_accounts(self) -> TransferCreate:
        if self.sender_id == self.receiver_id:
            raise ValueError("Sender and receiver must be different accounts.")

        return self


class TransferResponse(BaseModel):
    transfer_id: UUID
    created_at: datetime
    description: str
    entries: list[AccountEntryResponse]

    model_config = ConfigDict(from_attributes=True)