from passlib.context import CryptContext
from sqlmodel import select, Session

from app.models.user_models import User, UserRequest


def create_user(user_request: UserRequest, session: Session) -> User:
    user = User(**user_request.model_dump())
    user.password = create_password_hash(user_request.password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_id(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)

    if not user:
        raise ValueError("User not found")

    return user


def get_user_by_username(username: str, session: Session) -> User:
    query = select(User).where(User.username == username)
    user = session.exec(query).first()

    if not user:
        raise ValueError("Incorrect username")

    return user


def create_password_hash(password: str) -> str:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return password_context.hash(password)
