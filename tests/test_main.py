from fastapi import status
from fastapi.testclient import TestClient

from app.config.settings import settings


def test_root(test_client: TestClient) -> None:
    response = test_client.get(settings.root_path)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, World!"}
