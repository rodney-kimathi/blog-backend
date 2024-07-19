import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.post_models import Post


@pytest.mark.usefixtures("login")
class TestPostRead:
    def test_read_all(self, post: Post, test_client: TestClient) -> None:
        response = test_client.get("/posts")
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) > 0
        assert "id" in response_data[0]
        assert response_data[0]["title"] == post.title

    def test_read(self, post: Post, test_client: TestClient) -> None:
        response = test_client.get(f"/posts/{post.id}")
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response_data
        assert response_data["title"] == post.title

    def test_read_with_invalid_id(self, test_client: TestClient) -> None:
        response = test_client.get("/posts/0")
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["detail"] == "Post not found"
