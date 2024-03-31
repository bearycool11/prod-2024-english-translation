from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

import config

engine = create_engine(config.database_url, echo=True)
session_maker = sessionmaker(engine, expire_on_commit=False)


def load_models():
    from database.models import DBUser # noqa: unused
    from database.models import DBOrganization # noqa: unused


def get_session():
    with session_maker() as session:
        yield session


def init_models() -> None:
    load_models()
    with engine.begin() as conn:
        SQLModel.metadata.create_all(conn)
