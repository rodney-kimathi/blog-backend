from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.config.database import get_database_session
from app.models.access_models import Token
from app.models.user_models import User, UserRequest, UserResponse
from app.services.access_service import authenticate_user, create_access_token
from app.services.user_service import create_user

ACCESS_TOKEN_EXPIRY_HOURS = 24
SessionDependency = Annotated[Session, Depends(get_database_session)]
router = APIRouter(tags=["Access"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_request: UserRequest, session: SessionDependency) -> User:
    return create_user(user_request, session)


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDependency) -> Token:
    try:
        user = authenticate_user(form_data.username, form_data.password, session)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expiry = timedelta(hours=ACCESS_TOKEN_EXPIRY_HOURS)
    access_token = create_access_token(user.username, access_token_expiry)

    return Token(access_token=access_token, token_type="bearer")
