import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.post_models import PostRequest


@pytest.mark.usefixtures("login")
class TestPostCreate:
    def test_create(self, post_request: PostRequest, test_client: TestClient) -> None:
        response = test_client.post("/posts", json=post_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response_data
        assert response_data["title"] == post_request.title

    def test_create_with_incomplete_data(self, test_client: TestClient) -> None:
        response = test_client.post("/posts", json={})
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"] == ["body", "title"]

    def test_create_with_invalid_data(self, post_request: PostRequest, test_client: TestClient) -> None:
        post_request.title = "abc"
        response = test_client.post("/posts", json=post_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data["detail"][0]["msg"] == "String should have at least 4 characters"
        assert response_data["detail"][0]["type"] == "string_too_short"
        assert response_data["detail"][0]["loc"] == ["body", "title"]
