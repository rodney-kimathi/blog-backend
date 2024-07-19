import pytest

from app.models.user_models import User, UserRequest
from app.services.user_service import read_user_by_username


@pytest.fixture
def user_request() -> UserRequest:
    user_request = UserRequest(
        username="alan.turing",
        password="alanturing",
        email="alan@turing.ac.uk",
        full_name="Alan Turing"
    )

    return user_request


@pytest.fixture
def user(user_request: UserRequest, test_session) -> User:
    user = read_user_by_username(user_request.username, test_session)

    yield user
