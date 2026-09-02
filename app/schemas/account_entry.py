from decimal import Decimal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.models import EntryType

class AccountEntryResponse(BaseModel):
    entry_id: UUID
    user_id: UUID
    entry_type: EntryType
    amount: Decimal

    model_config = ConfigDict(from_attributes=True)
