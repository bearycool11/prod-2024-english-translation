from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.database_url, echo=False)
session_maker = sessionmaker(engine, expire_on_commit=False)


def get_session():
    return session_maker()
