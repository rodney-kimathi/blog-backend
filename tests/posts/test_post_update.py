import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.post_models import Post, PostRequest


@pytest.mark.usefixtures("login")
class TestPostUpdate:
    def test_update(self, post_request: PostRequest, post: Post, test_client: TestClient) -> None:
        post_request.title = "Updated title"
        post_request.content = "Updated content"
        response = test_client.put(f"/posts/{post.id}", json=post_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["title"] == post_request.title
        assert response_data["content"] == post_request.content
        assert response_data["created_at"] <= response_data["updated_at"]

    def test_update_with_invalid_id(self, post_request: PostRequest, test_client: TestClient) -> None:
        response = test_client.put("/posts/0", json=post_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["detail"] == "Post not found"

    def test_update_with_incomplete_data(self, post: Post, test_client: TestClient) -> None:
        response = test_client.put(f"/posts/{post.id}", json={})
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"] == ["body", "title"]

    def test_update_with_invalid_data(self, post_request: PostRequest, post: Post, test_client: TestClient) -> None:
        post_request.title = "abc"
        response = test_client.put(f"/posts/{post.id}", json=post_request.model_dump())
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data["detail"][0]["msg"] == "String should have at least 4 characters"
        assert response_data["detail"][0]["type"] == "string_too_short"
        assert response_data["detail"][0]["loc"] == ["body", "title"]
