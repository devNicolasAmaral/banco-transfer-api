from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Transfer
from app.schemas import TransferCreate, TransferResponse
from app.services import (
    InsufficientBalanceError,
    UserNotFoundError,
    create_transfer,
)


router = APIRouter(
    prefix="/transfers",
    tags=["transfers"],
)


@router.post(
    "",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transfer_endpoint(
    data: TransferCreate,
    session: Annotated[Session, Depends(get_db)],
) -> Transfer:
    try:
        return create_transfer(session, data)
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except InsufficientBalanceError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error