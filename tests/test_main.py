from fastapi import status
from fastapi.testclient import TestClient

from app.main import root_path


def test_root(test_client: TestClient) -> None:
    response = test_client.get(root_path)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, World!"}
