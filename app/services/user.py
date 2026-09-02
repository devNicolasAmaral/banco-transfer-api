from uuid import UUID

from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate

def create_user(session: Session, data: UserCreate) -> User:
    user = User(user_name=data.user_name)

    with session.begin():
        session.add(user)
        session.flush()

    return user

def get_user_by_id(session: Session, user_id: UUID) -> User | None:
    return session.get(User, user_id)
