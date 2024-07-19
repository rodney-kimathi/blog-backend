import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.access_models import TokenRequest
from app.models.user_models import UserRequest


@pytest.mark.usefixtures("signup")
class TestLogin:
    def test_login(
            self,
            user_request: UserRequest,
            token_request: TokenRequest,
            test_client: TestClient
    ) -> None:
        response = test_client.post("/login", json=token_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response_data

    def test_login_with_incorrect_username(
            self,
            user_request: UserRequest,
            token_request: TokenRequest,
            test_client: TestClient
    ) -> None:
        token_request.username = "incorrect_username"
        response = test_client.post("/login", json=token_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data["detail"] == "Incorrect username"

    def test_login_with_incorrect_password(
            self,
            user_request: UserRequest,
            token_request: TokenRequest,
            test_client: TestClient
    ) -> None:
        token_request.password = "incorrect_password"
        response = test_client.post("/login", json=token_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data["detail"] == "Incorrect password"
