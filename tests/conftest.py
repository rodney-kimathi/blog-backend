import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session

from app.config.database import get_database_session
from app.config.settings import settings
from app.main import app


@pytest.fixture(scope="session")
def test_session() -> Session:
    test_engine = create_engine(settings.test_db_url)
    alembic_config = Config("alembic.ini")
    alembic_config.attributes["connection"] = test_engine

    with Session(test_engine) as test_session:
        settings.env = "test"
        command.upgrade(alembic_config, "head")

        yield test_session

        command.downgrade(alembic_config, "base")
        settings.env = "dev"


@pytest.fixture
def test_client(test_session: Session) -> TestClient:
    def get_database_session_override():
        return test_session

    app.dependency_overrides[get_database_session] = get_database_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()
