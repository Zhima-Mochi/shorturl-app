import os
from get_docker_secret import get_docker_secret
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


# # get variables from environment variables
# HOST = os.environ["DB_HOST"]
# DATABASE_NAME = os.environ['DB_NAME']
# USER_NAME = os.environ['DB_USERNAME']
# PASSWORD = get_docker_secret('db_shorturl_password')

# SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?charset=utf8"
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///sqlite3/sqlite3.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    engine, expire_on_commit=False, autocommit=False, class_=AsyncSession)

Base = declarative_base()
