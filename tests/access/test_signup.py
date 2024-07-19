from fastapi import status
from fastapi.testclient import TestClient

from app.models.user_models import UserRequest


class TestSignup:
    def test_signup(self, user_request: UserRequest, test_client: TestClient) -> None:
        response = test_client.post("/signup", json=user_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert response_data["id"] is not None
        assert response_data["email"] == user_request.email
        assert "password" not in response_data

    def test_signup_with_incomplete_data(self, test_client: TestClient) -> None:
        response = test_client.post("/signup", json={})
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"] == ["body", "username"]

    def test_signup_with_invalid_data(self, user_request: UserRequest, test_client: TestClient) -> None:
        user_request.email = "invalid_email"
        response = test_client.post("/signup", json=user_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (response_data["detail"][0]["msg"] ==
                "value is not a valid email address: An email address must have an @-sign.")
        assert response_data["detail"][0]["type"] == "value_error"
        assert response_data["detail"][0]["loc"] == ["body", "email"]
