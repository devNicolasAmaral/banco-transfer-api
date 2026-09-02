from decimal import Decimal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class UserCreate(BaseModel):
    user_name: str = Field(
        min_length=3,
        max_length=30,
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class UserResponse(BaseModel):
    user_id: UUID
    user_name: str
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)
