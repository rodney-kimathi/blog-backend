from sqlalchemy import Engine
from sqlmodel import create_engine, Session

from app.config.settings import settings


def create_database_engine() -> Engine:
    return create_engine(settings.db_url)


def get_database_session() -> Session:
    engine = create_database_engine()

    with Session(engine) as session:
        yield session
