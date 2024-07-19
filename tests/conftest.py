import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text
from sqlmodel import create_engine, delete, Session

from app.config.database import get_database_session
from app.config.settings import settings
from app.main import app
from app.models.post_models import Post
from app.models.user_models import User

pytest_plugins = [
    "tests.fixtures.access_fixtures",
    "tests.fixtures.post_fixtures",
    "tests.fixtures.user_fixtures",
]


@pytest.fixture(scope="session")
def test_engine() -> Engine:
    engine = create_engine(settings.db_url, isolation_level="AUTOCOMMIT")

    with Session(engine) as session:
        statement = text(f"DROP DATABASE IF EXISTS {settings.test_db_name}")
        session.exec(statement)

        statement = text(f"CREATE DATABASE {settings.test_db_name}")
        session.exec(statement)

    test_engine = create_engine(settings.test_db_url)

    yield test_engine


@pytest.fixture
def test_session(test_engine: Engine) -> Session:
    alembic_config = Config("alembic.ini")

    with Session(test_engine) as test_session:
        settings.env = "test"
        alembic_config.attributes["connection"] = test_session.connection()
        command.upgrade(alembic_config, "head")

        yield test_session

        test_session.exec(delete(Post))
        test_session.exec(delete(User))
        test_session.commit()
        settings.env = "dev"


@pytest.fixture
def test_client(test_session: Session) -> TestClient:
    def get_database_session_override():
        return test_session

    app.dependency_overrides[get_database_session] = get_database_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()
