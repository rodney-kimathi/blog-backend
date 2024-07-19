import pytest

from app.models.user_models import UserRequest


@pytest.fixture
def user_request() -> UserRequest:
    user_request = UserRequest(
        username="alan.turing",
        password="alanturing",
        email="alan@turing.ac.uk",
        full_name="Alan Turing"
    )

    return user_request
