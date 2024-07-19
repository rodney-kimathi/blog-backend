from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.config.database import get_database_session
from app.config.security import get_current_active_user
from app.models.post_models import Post, PostRequest, PostResponse
from app.models.user_models import User
from app.services.post_service import create_post, read_post, read_posts, update_post

UserDependency = Annotated[User, Depends(get_current_active_user)]
SessionDependency = Annotated[Session, Depends(get_database_session)]
router = APIRouter(tags=["Posts"])


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create(post_request: PostRequest, current_user: UserDependency, session: SessionDependency) -> Post:
    return create_post(current_user.id, post_request, session)


@router.get("", response_model=list[PostResponse])
async def read_all(current_user: UserDependency, session: SessionDependency) -> list[Post]:
    return read_posts(current_user.id, session)


@router.get("/{post_id}", response_model=PostResponse)
async def read(post_id: int, current_user: UserDependency, session: SessionDependency) -> Post:
    try:
        return read_post(current_user.id, post_id, session)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.put("/{post_id}", response_model=PostResponse)
async def update(
    post_id: int,
    post_request: PostRequest,
    current_user: UserDependency,
    session: SessionDependency
) -> Post:
    try:
        return update_post(current_user.id, post_id, post_request, session)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
