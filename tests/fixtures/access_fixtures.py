import pytest
from fastapi.testclient import TestClient

from app.models.access_models import TokenRequest
from app.models.user_models import UserRequest


@pytest.fixture
def token_request(user_request: UserRequest) -> TokenRequest:
    token_request = TokenRequest(
        username=user_request.username,
        password=user_request.password,
    )

    return token_request


@pytest.fixture
def signup(user_request: UserRequest, test_client: TestClient) -> None:
    test_client.post("/signup", json=user_request.model_dump())


@pytest.fixture
def login(user_request: UserRequest, test_client: TestClient) -> None:
    test_client.post("/signup", json=user_request.model_dump())
    token = test_client.post("/login", data={"username": user_request.username, "password": user_request.password})
    token = token.json()["access_token"]
    test_client.headers.update({"Authorization": f"Bearer {token}"})
