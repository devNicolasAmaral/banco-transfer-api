from typing import Annotated
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.database import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserResponse,
)
from app.services import (
    create_user,
    get_user_by_id,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_endpoint(
    data: UserCreate,
    session: Annotated[Session, Depends(get_db)],
) -> User:
    return create_user(session, data)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_endpoint(
    user_id: UUID,
    session: Annotated[Session, Depends(get_db)],
) -> User:
    user = get_user_by_id(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found.",
        )

    return user