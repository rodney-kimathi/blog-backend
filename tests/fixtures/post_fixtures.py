import pytest

from app.models.post_models import PostRequest


@pytest.fixture
def post_request() -> PostRequest:
    post_request = PostRequest(
        title="Genesis",
        content="My first post",
    )

    return post_request
