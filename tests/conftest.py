import os

import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session

from app.config.database import get_database_session
from app.main import app

load_dotenv()


@pytest.fixture(scope="module")
def test_session() -> Session:
    test_connection_url = os.environ.get("TEST_DB_URL")
    test_engine = create_engine(test_connection_url)
    print(os.path.dirname(os.path.abspath(__file__)))

    with Session(test_engine) as test_session:
        alembic_config = Config("alembic.ini")
        alembic_config.set_main_option("sqlalchemy.url", os.environ.get("TEST_DB_URL"))
        command.upgrade(alembic_config, "head")
        yield test_session


@pytest.fixture(scope="module")
def test_client(test_session: Session) -> TestClient:
    def get_database_session_override():
        return test_session

    app.dependency_overrides[get_database_session] = get_database_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()
