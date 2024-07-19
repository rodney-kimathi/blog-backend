import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.post_models import Post


@pytest.mark.usefixtures("login")
class TestPostDelete:
    def test_delete(self, post: Post, test_client: TestClient) -> None:
        response = test_client.delete(f"/posts/{post.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = test_client.get(f"/posts/{post.id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_with_invalid_id(self, test_client: TestClient) -> None:
        response = test_client.delete("/posts/0")
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["detail"] == "Post not found"
