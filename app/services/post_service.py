from sqlmodel import Session

from app.models.post_models import Post, PostRequest
from app.services.user_service import get_user_by_id


def create_post(user_id: int, post_request: PostRequest, session: Session) -> Post:
    try:
        get_user_by_id(user_id, session)
    except ValueError as error:
        raise ValueError(str(error))

    post = Post(user_id=user_id, **post_request.model_dump())

    session.add(post)
    session.commit()
    session.refresh(post)

    return post
