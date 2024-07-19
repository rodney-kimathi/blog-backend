import pytest
from sqlmodel import Session

from app.models.post_models import Post, PostRequest
from app.models.user_models import User


@pytest.fixture
def post_request() -> PostRequest:
    post_request = PostRequest(
        title="Genesis",
        content="My first post",
    )

    return post_request


@pytest.fixture
def post(post_request: PostRequest, user: User, test_session: Session) -> Post:
    post = Post(user_id=user.id, **post_request.model_dump())

    test_session.add(post)
    test_session.commit()

    yield post
