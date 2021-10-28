from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from model import Base

SQLITE_DB_URL = "sqlite:///./sql_app.db"
DATABASE = SQLITE_DB_URL

ENGINE = create_engine(
    DATABASE
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base.query = session.query_property()

Base.metadata.create_all(bind=ENGINE)
