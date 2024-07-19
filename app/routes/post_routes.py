from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.config.database import get_database_session
from app.config.security import get_current_active_user
from app.models.post_models import Post, PostRequest, PostResponse
from app.models.user_models import User
from app.services.post_service import create_post

UserDependency = Annotated[User, Depends(get_current_active_user)]
SessionDependency = Annotated[Session, Depends(get_database_session)]
router = APIRouter(tags=["Posts"])


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create(post_request: PostRequest, current_user: UserDependency, session: SessionDependency) -> Post:
    try:
        return create_post(current_user.id, post_request, session)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
