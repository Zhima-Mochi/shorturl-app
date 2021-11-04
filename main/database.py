from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os
from get_docker_secret import get_docker_secret

# get variables from environment variables
HOST = "db"
DATABASE_NAME = os.environ['DB_NAME']
USER_NAME = os.environ['DB_USERNAME']
PASSWORD = get_docker_secret('db_shorturl_password')

SQLALCHEMY_DATABASE_URL = f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?charset=utf8"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# SessionLocal = scoped_session(
#     sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=engine
#     )
# )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
