from datetime import timedelta

import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from app.config.settings import settings
from app.models.user_models import User
from app.services.user_service import read_user_by_username
from app.utils.date_utils import datetime_now_utc


def create_access_token(username: str, expiry_delta: timedelta) -> str:
    data = {"sub": username}
    expiry = datetime_now_utc() + expiry_delta
    data.update({"exp": expiry})

    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def authenticate_user(username: str, password: str, session: Session) -> User:
    try:
        user = read_user_by_username(username, session)
    except ValueError as error:
        raise ValueError(str(error))

    if not is_password_valid(password, user.password):
        raise ValueError("Incorrect password")

    return user


def is_password_valid(plain_password: str, hashed_password: str) -> bool:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return password_context.verify(plain_password, hashed_password)
