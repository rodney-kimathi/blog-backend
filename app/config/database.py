import os

from sqlalchemy import Engine
from sqlmodel import create_engine, Session


def create_database_engine() -> Engine:
    connection_url = os.environ.get("DB_URL")

    return create_engine(connection_url)


def get_database_session() -> Session:
    engine = create_database_engine()

    with Session(engine) as session:
        yield session
