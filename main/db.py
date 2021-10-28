from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from model import Base
import os
from get_docker_secret import get_docker_secret

HOST = "db"
DATABASE_NAME = os.environ['DB_NAME']
USER_NAME = os.environ['DB_USERNAME']
PASSWORD = get_docker_secret('db_shorturl_password')

DATABASE = f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?charset=utf8"

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


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
